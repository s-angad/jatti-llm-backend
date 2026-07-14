from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ContextBundle:
    grammar_rules: str
    syntax_docs: str
    examples: str
    test_cases: str

    def as_prompt_block(self) -> str:
        return (
            "[Grammar Rules]\n"
            f"{self.grammar_rules.strip()}\n\n"
            "[Syntax Docs]\n"
            f"{self.syntax_docs.strip()}\n\n"
            "[Example Programs]\n"
            f"{self.examples.strip()}\n\n"
            "[Compiler Test Cases]\n"
            f"{self.test_cases.strip()}\n"
        )


class ContextStore:
    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or Path(__file__).resolve().parent.parent / "data"

    def _read_text(self, name: str) -> str:
        path = self.data_dir / name
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def _read_jsonl(self, name: str) -> List[dict]:
        path = self.data_dir / name
        rows: List[dict] = []
        if not path.exists():
            return rows
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
        return rows

    def load(self) -> ContextBundle:
        examples = self._read_jsonl("examples.jsonl")
        tests = self._read_jsonl("compiler_test_cases.jsonl")

        example_text = []
        for item in examples:
            example_text.append(
                f"Prompt: {item.get('prompt', '')}\nCode:\n{item.get('code', '').strip()}"
            )

        test_text = []
        for item in tests:
            test_text.append(
                f"Input: {item.get('input', '')}\nExpected: {item.get('expected', '')}\nNotes: {item.get('notes', '')}"
            )

        return ContextBundle(
            grammar_rules=self._read_text("grammar_rules.md"),
            syntax_docs=self._read_text("syntax_docs.md"),
            examples="\n\n".join(example_text),
            test_cases="\n\n".join(test_text),
        )
