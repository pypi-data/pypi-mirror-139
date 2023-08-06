#!/usr/bin/env python3

import re
from subprocess import check_output


def get_out(cmd):
    return check_output(cmd, shell=True).decode("utf-8").strip()


with open("tsvkit/__init__.py", encoding="utf-8") as f:
    version = re.search(r'__version__\s*=\s*"(.*)"', f.read()).group(1)

help_cmd = "tsvkit --help"
help_out = get_out(help_cmd)

head_cmd = "head data/data.tsv"
head_out = get_out(head_cmd)

header_cmd = "tsvkit -H data/data.tsv"
header_out = get_out(header_cmd)

view_cmmd_1 = "head data/data.tsv | tsvkit -v"
view_out_1 = get_out(view_cmmd_1)

view_cmd_2 = "head data/data.tsv | tsvkit -v -w 5"
view_out_2 = get_out(view_cmd_2)

stat_cmd = "tsvkit -s -H -v data/data.tsv"
stat_out = get_out(stat_cmd)

pattern_cmd = "cat data/data.tsv | tsvkit -p 'int($1)<20 and $5.startswith(\"0.1\")' -v -H"
pattern_out = get_out(pattern_cmd)

add_cmd = "cat data/data.tsv | tsvkit -H -a 'int($1)+int($2)' -v | head"
add_out = get_out(add_cmd)

reorder_cmd = "cat data/data.tsv | tsvkit -r 2,3,1,1 -v | head"
reorder_out = get_out(reorder_cmd)

xlsx_cmd = "tsvkit data/data.xlsx -r 2,3,1,1 -v | head"
xlsx_out = get_out(xlsx_cmd)

text = f"""# tsvkit

TSV toolkit: print header, aligned display, descriptive statistics, pattern match, add a column, reorder columns, supports TSV, CSV, XLS and XLSX

## Installation

```
pip install tsvkit=={version}
```

## Usage

```
$ {help_cmd}
{help_out}
```

## Example

```
$ {head_cmd}
{head_out}
```

### print header or include header in output

```
$ {header_cmd}
{header_out}
```

### aligned display of each column

```
$ {view_cmmd_1}
{view_out_1}

$ {view_cmd_2}
{view_out_2}
```

### descriptive statistics

```
$ {stat_cmd}
{stat_out}
```

### pattern to match

```
$ {pattern_cmd}
{pattern_out}
```

### add a new column with pattern

```
$ {add_cmd}
{add_out}
```

### reorder columns

```
$ {reorder_cmd}
{reorder_out}
```

###  all functions support CSV, XLS and XLSX, by specifying the file name

```
$ {xlsx_cmd}
{xlsx_out}
```
"""

print(text)
