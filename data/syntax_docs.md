# Jatti Syntax Docs

## Program wrapper
```jatti
sun_we
    chilla_we "Hello Jatti!"
ja_we
```

## Assignment and print
```jatti
sun_we
    chal_oye x ban 10
    chilla_we x
ja_we
```

## Function and return
```jatti
sun_we
    kaam add(a, b)
        wapas_kar a + b

    chal_oye result ban add(5, 3)
    chilla_we result
ja_we
```

## If / else
```jatti
sun_we
    chal_oye score ban 85
    je score vadha_ya_barabar 80
        chilla_we "Pass"
    nahin_taan
        chilla_we "Fail"
ja_we
```

## Loop with range
```jatti
sun_we
    har_ek i range_banao(1, 6)
        chilla_we i
ja_we
```

## Loop with list
```jatti
sun_we
    chal_oye numbers ban [10, 20, 30]
    har_ek num numbers
        chilla_we num
ja_we
```

## While loop
```jatti
sun_we
    chal_oye count ban 1
    jadon_tak count vadha_hai 5
        chilla_we count
        chal_oye count ban count + 1
ja_we
```

## Loop with accumulator
```jatti
sun_we
    chal_oye total ban 0
    har_ek i range_banao(1, 6)
        chal_oye total ban total + i
    chilla_we total
ja_we
```

## List and dictionary access
```jatti
sun_we
    chal_oye items ban [1, 2, 3, 4]
    chal_oye person ban {"name": "Singh", "age": 25}
    chilla_we kinna_lamba(items)
    chilla_we person["name"]
ja_we
```

## String methods
```jatti
sun_we
    chal_oye text ban "Jatti Programming"
    chilla_we vada_likha(text)
    chilla_we chhota_likha(text)
    chal_oye words ban vand_karo(text, " ")
    chilla_we words
ja_we
```

## Function returning words
```jatti
sun_we
    kaam shabd_kadho(sentence)
        wapas_kar vand_karo(sentence, " ")

    chal_oye words ban shabd_kadho("this is a sentence")
    chilla_we words
ja_we
```

## Palindrome string
```jatti
sun_we
    chal_oye text ban "level"
    chal_oye chars ban vand_karo(text, "")
    chal_oye rev ban ""
    har_ek ch chars
        chal_oye rev ban ch + rev
    je text barabar rev
        chilla_we "Palindrome"
    nahin_taan
        chilla_we "Not palindrome"
ja_we
```

## Even numbers loop
```jatti
sun_we
    har_ek i range_banao(1, 11)
        je i % 2 barabar 0
            chilla_we i
ja_we
```

## While counter loop
```jatti
sun_we
    chal_oye count ban 1
    jadon_tak count vadha_hai 5
        chilla_we count
        chal_oye count ban count + 1
ja_we
```

## Nested loops
```jatti
sun_we
    har_ek i range_banao(1, 3)
        har_ek j range_banao(1, 4)
            chilla_we i * j
ja_we
```

## Boolean function
```jatti
sun_we
    kaam is_even(n)
        je n % 2 barabar 0
            wapas_kar sach
        nahin_taan
            wapas_kar jhoot

    chilla_we is_even(4)
ja_we
```

## Try / catch
```jatti
sun_we
    chal_koshish_karle
        chilla_we 10 / 0
    pakad err
        chilla_we err
ja_we
```

## File I/O
```jatti
sun_we
    likh("output.txt", "Hello from Jatti!")
    chal_oye content ban padh("output.txt")
    chilla_we content
ja_we
```
