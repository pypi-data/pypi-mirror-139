# csvdivider
csvdivider is a command-line tool for dividing CSV into separated CSVs
## Example
```bash

csvdivide xxx.csv 1000

#more
csvdivide -h
usage: csvdivide [-h] [-i INPUT_FILE] [-o [OUTPUT_PATH]] [--head | --no-head] lines

Dividing CSV into separated CSVs.

positional arguments:
  lines                 Insert a column of line numbers at the front of the output.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        The CSV file to operate on.
  -o [OUTPUT_PATH], --output_path [OUTPUT_PATH]
                        output folder
  --head, --no-head     with or without column names, default value: True
```
## Installing threado and Supported Versions

threado is available on PyPI:

```console
$ python -m pip install csvdivider
```