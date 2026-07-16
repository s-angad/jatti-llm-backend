# Jatti Grammar Rules

## Program shape
- Start every full program with `sun_we`
- End every full program with `ja_we`
- Use 4 spaces for indentation
- Prefer one clear action per line

## Core statements
- `chal_oye name ban expr` for assignment
- `chilla_we expr` for output
- `je expr` for if
- `nahin_taan_je expr` for else-if
- `nahin_taan` for else
- `jadon_tak expr` for while
- `har_ek item collection` for iteration
- `kaam name(params)` for functions
- `wapas_kar expr` for returns
- `chal_koshish_karle` for try
- `pakad err` for catch

## Common patterns
- Hello world: `sun_we` ... `chilla_we "Hello"` ... `ja_we`
- For loop (range): `har_ek i range_banao(1, 6)` then indent body
- For loop (list): `har_ek item list_name` then indent body
- While loop: `jadon_tak condition` then indent body
- Loop with condition: use `je` inside loop body
- Accumulator: `chal_oye total ban 0` then `chal_oye total ban total + value` in loop
- Factorial: recursive `kaam factorial(n)` with `wapas_kar`
- Decision: `je` ... `nahin_taan` ...
- Errors: `chal_koshish_karle` + `pakad`
- Strings: `vada_likha`, `chhota_likha`, `vand_karo`, `badal_de`
- Collections: lists `[]`, dictionaries `{}`

## Operators
- Arithmetic: `+ - * / % **`
- Comparison: `vadha_hai`, `nikka_hai`, `barabar`, `barabar_nahi_hai`, `vadha_ya_barabar`, `nikka_ya_barabar`
- Logic: `ate`, `ya_te`, `nahi`

## Literals
- Strings: `"text"` or `'text'`
- Numbers: integers and floats
- Booleans: `sach`, `jhoot`
- Null: `khaali`
- Lists: `[1, 2, 3]`
- Dictionaries: `{ "name": "Singh" }`

## Built-ins and helpers
- `range_banao`, `kinna_lamba`, `kism`, `likh`, `padh`, `dasso` (user input), `number`
- `sab_ton_vaddha`, `sab_ton_chhota`
- `sorted`, `reversed`
- `vada_likha`, `chhota_likha`, `saf_karo`, `vand_karo`, `badal_de`, `shuru_hunda`, `khatam_hunda`, `dhundh_ja`

## Best output rule
- If a user asks for code, return a complete valid Jatti program unless they explicitly ask for a snippet

## ANTI-HALLUCINATION & STRICT SYNTAX (CRITICAL)
- **DO NOT** use Python or JavaScript keywords.
- **NEVER** use `=` for assignment. ALWAYS use `chal_oye <name> ban <expr>`.
- **NEVER** use `def` or `function`. ALWAYS use `kaam <name>(<params>)`.
- **NEVER** use `if`, `elif`, `else`. ALWAYS use `je`, `nahin_taan_je`, `nahin_taan`.
- **NEVER** use `while` or `for`. ALWAYS use `jadon_tak` and `har_ek`.
- **NEVER** use `==`, `<`, `>`. ALWAYS use `barabar`, `nikka_hai`, `vadha_hai`.
- **NEVER** use inline conditionals (ternary operators). `je` MUST be a block on its own line. Example of FORBIDDEN: `chal_oye x ban je a sach nahin_taan jhoot`.
- **NEVER** use `print()`. ALWAYS use `chilla_we <expr>`.
- **NEVER** use `True` or `False`. ALWAYS use `sach` or `jhoot`.
- **NEVER** forget `sun_we` at the start and `ja_we` at the end of a full program.
- **IMPORTANT**: The `dasso()` function returns a string. You MUST use `number()` to convert the input to a number BEFORE comparing it with `vadha_hai`, `nikka_hai`, `vadha_ya_barabar`, `nikka_ya_barabar` or performing math. Example: `chal_oye age ban number(dasso("Age: "))`.

- **NEVER** use `ja_we` to close loops (`har_ek`, `jadon_tak`), functions (`kaam`), or if-blocks (`je`). Blocks are closed PURELY by reducing the indentation level! `ja_we` is ONLY used exactly ONCE at the very end of the program.
- **ALWAYS** spell `dasso` with double s. NEVER write `daso`. AND ALWAYS pass a string argument to it (e.g., `dasso("Enter name: ")`).