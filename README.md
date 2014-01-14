otm
===

otm - display static memory of an elf file in a treemap

Produces output like this: ![msb-430 space consumption](http://ludwig.spline.inf.fu-berlin.de/riot/nm/wobj/default_msb-430_nm.jpg)

Needs python2, scipy, matplotlib, binutils (nm).
Best used with an elf with debugging symbols as input.

usage
=====

```
usage: otm.py [-h] [-d] [-f FUNCTION_PATH_REGEX] [-o OBJECT_PATH_REGEX]
              [-F FUNCTION_NAME_REGEX] [-O OBJECT_NAME_REGEX]
              [-t SYMBOL_TYPE_LIST] [-m MINIMUM_SIZE]
              [filename]

otm - display static memory of an elf file in a treemap

positional arguments:
  filename              the elf file to parse

optional arguments:
  -h, --help            show this help message and exit
  -d, --documentation   print additional documentation and exit
  -f FUNCTION_PATH_REGEX, --function-path-regex FUNCTION_PATH_REGEX
                        regular expression for function path filtering
  -o OBJECT_PATH_REGEX, --object-path-regex OBJECT_PATH_REGEX
                        regular expression for object path filtering
  -F FUNCTION_NAME_REGEX, --function-name-regex FUNCTION_NAME_REGEX
                        regular expression for function name filtering
  -O OBJECT_NAME_REGEX, --object-name-regex OBJECT_NAME_REGEX
                        regular expression for object name filtering
  -t SYMBOL_TYPE_LIST, --symbol-type-list SYMBOL_TYPE_LIST
                        list of symbol types to include
  -m MINIMUM_SIZE, --minimum-size MINIMUM_SIZE
                        mininum size for all types
```

documentation
=============

```
Regular expression examples:
  --func-path-regex "net|core"  # display any function that comes from net or core
  --obj-path-regex "\?\?"       # display only objects that nm could not look up
  --obj-name-regex "stack"      # display only objects named *stack*

Symbol type list:
  --symbol-type-list tTbB  # include text and BSS section symbols
                             check the nm manpage for details

Minumum size:
  The minimum-size argument is taken as an inclusion hurdle, i.e.
  symbols below that size are not taken into consideration at all.
```
