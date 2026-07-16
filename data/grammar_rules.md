# Jatti Grammar Rules

## Program shape
- Start every full program with sun_we
- End every full program with ja_we
- Use 4 spaces for indentation
- Prefer one clear action per line

## Core statements
- chal_oye name ban expr for assignment
- chilla_we expr for output
- je expr for if
- 
ahin_taan_je expr for else-if
- 
ahin_taan for else
- jadon_tak expr for while
- har_ek item collection for iteration
- kaam name(params) for functions
- wapas_kar expr for returns
- chal_koshish_karle for try
- pakad err for catch

## Common patterns
- Hello world: sun_we ... chilla_we "Hello" ... ja_we
- For loop (range): har_ek i range_banao(1, 6) then indent body
- For loop (list): har_ek item list_name then indent body
- While loop: jadon_tak condition then indent body
- Loop with condition: use je inside loop body
- Accumulator: chal_oye total ban 0 then chal_oye total ban total + value in loop
- Factorial: recursive kaam factorial(n) with wapas_kar
- Decision: je ... nahin_taan ...
- Errors: chal_koshish_karle + pakad
- Strings: ada_likha, chhota_likha, and_karo, adal_de
- Collections: lists [], dictionaries {}

## Operators
- Arithmetic: + - * / % **
- Comparison: adha_hai, 
ikka_hai, arabar, arabar_nahi_hai, adha_ya_barabar, 
ikka_ya_barabar
- Logic: te, ya_te, 
ahi

## Literals
- Strings: "text" or 'text'
- Numbers: integers and floats
- Booleans: sach, jhoot
- Null: khaali
- Lists: [1, 2, 3]
- Dictionaries: { "name": "Singh" }

## Built-ins and helpers
- 
ange_banao, kinna_lamba, kism, likh, padh, dasso (user input), ganao
- sab_ton_vaddha, sab_ton_chhota
- sorted, 
eversed
- ada_likha, chhota_likha, saf_karo, and_karo, adal_de, shuru_hunda, khatam_hunda, dhundh_ja

## Best output rule
- If a user asks for code, return a complete valid Jatti program unless they explicitly ask for a snippet

## ANTI-HALLUCINATION & STRICT SYNTAX (CRITICAL)
- **DO NOT** use Python or JavaScript keywords.
- **NEVER** use = for assignment. ALWAYS use chal_oye <name> ban <expr>.
- **NEVER** use def or unction. ALWAYS use kaam <name>(<params>).
- **NEVER** use if, elif, else. ALWAYS use je, 
ahin_taan_je, 
ahin_taan.
- **NEVER** use while or or. ALWAYS use jadon_tak and har_ek.
- **NEVER** use ==, <, >. ALWAYS use arabar, 
ikka_hai, adha_hai.
- **NEVER** use inline conditionals (ternary operators). je MUST be a block on its own line. Example of FORBIDDEN: chal_oye x ban je a sach nahin_taan jhoot.
- **NEVER** use print(). ALWAYS use chilla_we <expr>.
- **NEVER** use True or False. ALWAYS use sach or jhoot.
- **NEVER** forget sun_we at the start and ja_we at the end of a full program.
