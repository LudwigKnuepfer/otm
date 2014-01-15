otm
===

otm - display static memory of an elf file in a treemap

Produces output like this: ![msb-430 space consumption](http://ludwig.spline.inf.fu-berlin.de/riot/nm/wobj/default_msb-430_nm.jpg)

Needs python2, scipy, matplotlib, binutils (nm).
Best used with an elf with debugging symbols as input.

usage
=====

```
usage: otm.py [-h] [-d] [-fp FUNCTION_PATH_REGEX_IN]
              [-op OBJECT_PATH_REGEX_IN] [-fn FUNCTION_NAME_REGEX_IN]
              [-on OBJECT_NAME_REGEX_IN] [-Fp FUNCTION_PATH_REGEX_EX]
              [-Op OBJECT_PATH_REGEX_EX] [-Fn FUNCTION_NAME_REGEX_EX]
              [-On OBJECT_NAME_REGEX_EX] [-t SYMBOL_TYPE_LIST]
              [-m MINIMUM_SIZE]
              [filename]

otm - display static memory of an elf file in a treemap

positional arguments:
  filename              the elf file to parse

optional arguments:
  -h, --help            show this help message and exit
  -d, --documentation   print additional documentation and exit
  -fp FUNCTION_PATH_REGEX_IN, --function-path-regex-in FUNCTION_PATH_REGEX_IN
                        regular expression for function path inclusion
  -op OBJECT_PATH_REGEX_IN, --object-path-regex-in OBJECT_PATH_REGEX_IN
                        regular expression for object path inclusion
  -fn FUNCTION_NAME_REGEX_IN, --function-name-regex-in FUNCTION_NAME_REGEX_IN
                        regular expression for function name inclusion
  -on OBJECT_NAME_REGEX_IN, --object-name-regex-in OBJECT_NAME_REGEX_IN
                        regular expression for object name inclusion
  -Fp FUNCTION_PATH_REGEX_EX, --function-path-regex-ex FUNCTION_PATH_REGEX_EX
                        regular expression for function path exclusion
  -Op OBJECT_PATH_REGEX_EX, --object-path-regex-ex OBJECT_PATH_REGEX_EX
                        regular expression for object path exclusion
  -Fn FUNCTION_NAME_REGEX_EX, --function-name-regex-ex FUNCTION_NAME_REGEX_EX
                        regular expression for function name exclusion
  -On OBJECT_NAME_REGEX_EX, --object-name-regex-ex OBJECT_NAME_REGEX_EX
                        regular expression for object name exclusion
  -t SYMBOL_TYPE_LIST, --symbol-type-list SYMBOL_TYPE_LIST
                        list of symbol types to include
  -m MINIMUM_SIZE, --minimum-size MINIMUM_SIZE
                        mininum size for all types
```

documentation
=============

```
Regular expression examples:
    display only functions that come from net or core:
        --function-path-regex-in "net|core"

    display only objects that nm could not look up
        --obj-path-regex "\?\?"

    do not display objects that end on _stack
        --object-name-regex-ex "_stack$"

    When combining these options, exclusion takes precedence over
    inclusion:

    display only objects from main.c filtering out stacks:
        -op "main\.c" -On "_stack$|_stk$"


Symbol type list:
    include text and BSS section symbols check the nm manpage for
    details:
        --symbol-type-list tTbB


Minumum size:
    The minimum-size argument is taken as an inclusion hurdle, i.e.
    symbols below that size are not taken into consideration at all.

```
