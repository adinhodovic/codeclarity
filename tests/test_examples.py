"""Check example contracts that syntax-only validation cannot protect."""

import ast
import doctest
from pathlib import Path
import re
import runpy
from types import SimpleNamespace
import unittest


ROOT = Path(__file__).resolve().parents[1]
HEADER = re.compile(r"^# --- (.+) ---$", re.MULTILINE)


def sections(text):
    parts = HEADER.split(text)
    return dict(zip(parts[1::2], parts[2::2]))


class WithoutDocumentation(ast.NodeTransformer):
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return None
        return self.generic_visit(node)


class ExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {
            name: (ROOT / "references" / f"{name}.py").read_text()
            for name in ("before", "after")
        }
        cls.examples = {name: sections(text) for name, text in cls.sources.items()}
        cls.namespaces = {
            name: runpy.run_path(str(ROOT / "references" / f"{name}.py"))
            for name in cls.sources
        }

    def test_headers_match_skill(self):
        skill = (ROOT / "SKILL.md").read_text()
        headings = set(re.findall(r"^#{3,4} (.+)$", skill, re.MULTILINE))
        headers = HEADER.findall(self.sources["before"])
        self.assertEqual(headers, HEADER.findall(self.sources["after"]))
        self.assertEqual(len(headers), len(set(headers)), "Duplicate example headers")
        for header in headers:
            self.assertIn(header.split(": ", 1)[1], headings)
        self.assertNotIn("```", skill, "Keep worked examples in references/")

    def test_documentation_edits_preserve_executable_code(self):
        authorized_code_changes = {
            "Comments: Replace a comment with a name",
            "Generic guidelines and gotchas: Spell out terse idioms",
            "Generic guidelines and gotchas: Apply one rule in one place",
            "Tests: Let test names carry the scenario",
            "Names: Name the behavior",
            "Names: Rename safely",
            "Names: Avoid relative and implementation words",
            "Names: Name a limit by what it bounds",
            "Names: Keep one name for one value",
        }
        for header, before in self.examples["before"].items():
            if header in authorized_code_changes:
                continue
            with self.subTest(header=header):
                trees = [
                    ast.dump(WithoutDocumentation().visit(ast.parse(source)))
                    for source in (before, self.examples["after"][header])
                ]
                self.assertEqual(*trees)

    def test_functional_comments_keep_placement(self):
        header = "Generic guidelines and gotchas: Preserve functional comments"
        for marker in ("SPDX-License-Identifier:", "# noqa:", "# nosec"):
            lines = [
                [line for line in self.examples[name][header].splitlines() if marker in line]
                for name in ("before", "after")
            ]
            self.assertTrue(lines[0])
            self.assertEqual(*lines)

    def test_extraction_preserves_short_circuiting_and_access_order(self):
        class RecordProbe:
            def __init__(self, values):
                self.values = values
                self.reads = []

            def __getattr__(self, name):
                self.reads.append(name)
                if name not in self.values:
                    raise AttributeError(name)
                return self.values[name]

        cases = [
            ({"status": "inactive"}, ["status"], False),
            ({"status": "active", "owner_tenant": None}, ["status", "owner_tenant"], False),
            ({"status": "active", "owner_tenant": "tenant", "reviewed_this_quarter": True},
             ["status", "owner_tenant", "reviewed_this_quarter"], False),
            ({"status": "active", "owner_tenant": "tenant", "reviewed_this_quarter": False},
             ["status", "owner_tenant", "reviewed_this_quarter"], True),
        ]
        for name, namespace in self.namespaces.items():
            for values, reads, queued in cases:
                with self.subTest(version=name, values=values):
                    record = RecordProbe(values)
                    queue = []
                    namespace["queue_for_review"](record, queue)
                    self.assertEqual(record.reads, reads)
                    self.assertEqual(queue, [record] if queued else [])

    def test_renames_preserve_selection_and_wire_keys(self):
        inactive = SimpleNamespace(active=False)
        active = SimpleNamespace(active=True)
        for name, function in (("before", "process"), ("after", "select_active_items")):
            with self.subTest(version=name):
                namespace = self.namespaces[name]
                self.assertEqual(namespace[function]([inactive, active]), [active])
                self.assertEqual(namespace["UserPayload"](42).to_wire(), {"user_id": 42})
        self.namespaces["before"]["test_it"]()
        self.namespaces["after"]["test_zero_limit_leaves_input_unchanged"]()

    def test_renamed_limits_and_parameters_keep_results(self):
        photos = [SimpleNamespace(pixels=index) for index in range(7)]
        reviews = [SimpleNamespace(product_id="a")]
        products = [SimpleNamespace(product_id=code) for code in ("a", "b")]
        for name, namespace in self.namespaces.items():
            with self.subTest(version=name):
                self.assertEqual(namespace["album_thumbnails"](photos), [0, 1, 2, 3, 4])
                self.assertEqual(namespace["_recommend"](products, reviews), products[1:])
                count = namespace["capped_comment_count"]
                self.assertEqual(count(list(range(10))), (10, False))
                self.assertEqual(count(list(range(11))), (10, True))

    def test_fallback_contracts_include_falsy_values(self):
        for name, namespace in self.namespaces.items():
            for override in (None, False, 0, "", []):
                with self.subTest(version=name, override=override):
                    scope = SimpleNamespace(override=override, default="default")
                    self.assertEqual(namespace["apply_override"](scope), "default")
                    self.assertIs(scope.override, override)
                    record = SimpleNamespace(override=override, default=0, legacy="legacy")
                    self.assertEqual(namespace["select_value"](record), "legacy")
            self.assertEqual(namespace["select_value"](
                SimpleNamespace(override=None, default=0, legacy=[])), [])

    def test_plain_idiom_keeps_every_result(self):
        for measurement in ("10 px", "10", "", "10 px extra"):
            with self.subTest(measurement=measurement):
                self.assertEqual(
                    self.namespaces["before"]["unit_of"](measurement),
                    self.namespaces["after"]["unit_of"](measurement),
                )

    def test_one_rule_keeps_every_result(self):
        forms = [
            {"tags": "red, !secret, ,blue"},
            {"tag.1": " green ", "tag.2": "!hidden", "tag.3": "  "},
            {"tags": "a,b", "tag.1": "c", "other": "x"},
            {},
        ]
        for fields in forms:
            with self.subTest(fields=fields):
                self.assertEqual(
                    self.namespaces["before"]["public_tags"](fields),
                    self.namespaces["after"]["public_tags"](fields),
                )

    def test_parser_examples_are_executable(self):
        namespace = self.namespaces["after"]
        test = doctest.DocTestParser().get_doctest(
            namespace["parse_size"].__doc__, namespace, "parse_size", "after.py", 0
        )
        result = doctest.DocTestRunner(verbose=False).run(test)
        self.assertEqual(result.failed, 0)
        self.assertEqual(result.attempted, 3)

    def test_useful_example_is_executable(self):
        for name, namespace in self.namespaces.items():
            with self.subTest(version=name):
                function = namespace["group_pairs"]
                test = doctest.DocTestParser().get_doctest(
                    function.__doc__, namespace, "group_pairs", f"{name}.py", 0
                )
                result = doctest.DocTestRunner(verbose=False).run(test)
                self.assertEqual(result.failed, 0)
                self.assertGreater(result.attempted, 0)


if __name__ == "__main__":
    unittest.main()
