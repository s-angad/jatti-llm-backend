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
- Hello world: `sun_we ... chilla_we "Hello" ... ja_we`
- For loop (range): `har_ek i range_banao(1, 6)` then indent body
- For loop (list): `har_ek item list_name` then indent body
- While loop: `jadon_tak condition` then indent body
- Loop with condition: use `je` inside loop body
- Accumulator: `chal_oye total ban 0` then `chal_oye total ban total + value` in loop
- Factorial: recursive `kaam factorial(n)` with `wapas_kar`
- Decision: `je ... nahin_taan ...`
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
- `range_banao`, `kinna_lamba`, `kism`, `likh`, `padh`, `ganao`
- `sab_ton_vaddha`, `sab_ton_chhota`
- `sorted`, `reversed`
- `vada_likha`, `chhota_likha`, `saf_karo`, `vand_karo`, `badal_de`, `shuru_hunda`, `khatam_hunda`, `dhundh_ja`

## Best output rule
- If a user asks for code, return a complete valid Jatti program unless they explicitly ask for a snippet
