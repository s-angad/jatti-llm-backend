from __future__ import annotations

from dataclasses import dataclass
from typing import List


KEYWORDS = {
    "sun_we",
    "ja_we",
    "chal_oye",
    "ban",
    "chilla_we",
    "fuddu_chiz",
    "je",
    "nahin_taan_je",
    "nahin_taan",
    "har_ek",
    "jadon_tak",
    "roko_oye_roko",
    "chalo_oye_chalo",
    "kaam",
    "wapas_kar",
    "chal_koshish_karle",
    "pakad",
}


@dataclass
class Token:
    kind: str
    value: str
    line: int


class Lexer:
    def lex(self, code: str) -> List[Token]:
        tokens: List[Token] = []
        for lineno, raw in enumerate(code.splitlines(), start=1):
            line = raw.split("#", 1)[0].strip()
            if not line or line.startswith("fuddu_chiz"):
                continue
            for part in line.replace("(", " (").replace(")", ") ").replace(",", " , ").split():
                kind = "keyword" if part in KEYWORDS else "symbol"
                tokens.append(Token(kind=kind, value=part, line=lineno))
        return tokens


class Parser:
    def parse(self, code: str) -> List[str]:
        errors: List[str] = []
        lines = code.splitlines()
        meaningful = [(i + 1, ln.rstrip()) for i, ln in enumerate(lines) if ln.strip()]
        if not meaningful:
            return ["Empty program."]

        if not meaningful[0][1].lstrip().startswith("sun_we"):
            errors.append(f"Line {meaningful[0][0]}: program must start with sun_we.")

        if not meaningful[-1][1].lstrip().startswith("ja_we"):
            errors.append(f"Line {meaningful[-1][0]}: program must end with ja_we.")

        for line_no, raw in meaningful:
            indent = len(raw) - len(raw.lstrip(" "))
            if indent % 4 != 0:
                errors.append(f"Line {line_no}: indentation must use multiples of 4 spaces.")
            if "\t" in raw[:indent]:
                errors.append(f"Line {line_no}: tabs are not allowed in indentation.")

        return errors


class Compiler:
    def compile(self, code: str) -> List[str]:
        errors: List[str] = []
        for line_no, raw in enumerate(code.splitlines(), start=1):
            stripped = raw.strip()
            if not stripped or stripped.startswith("fuddu_chiz"):
                continue

            if stripped.startswith("chal_oye") and " ban " not in stripped:
                errors.append(f"Line {line_no}: chal_oye assignments must use ban.")
            if stripped.startswith("kaam") and "(" not in stripped:
                errors.append(f"Line {line_no}: kaam requires a parameter list.")
            if stripped.startswith("pakad") and len(stripped.split()) < 2:
                errors.append(f"Line {line_no}: pakad requires an error variable name.")
            if stripped.startswith("har_ek") and len(stripped.split()) < 3:
                errors.append(f"Line {line_no}: har_ek requires an iterator target and collection.")

        return errors


class JattiValidator:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.compiler = Compiler()

    def validate(self, code: str) -> List[str]:
        errors: List[str] = []
        self.lexer.lex(code)
        errors.extend(self.parser.parse(code))
        errors.extend(self.compiler.compile(code))
        return errors
