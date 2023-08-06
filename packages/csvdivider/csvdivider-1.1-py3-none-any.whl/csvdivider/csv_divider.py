import os
import argparse

from typing import List, Generator

parser = argparse.ArgumentParser(description='Dividing CSV into separated CSVs.')

parser.add_argument('lines', type=int,
                    help='Insert a column of line numbers at the front of the output.')

parser.add_argument('-i', '--input_file', dest='input_file',
                    help='The CSV file to operate on. ')

parser.add_argument('-o', '--output_path', dest='output_path', nargs='?',
                    help='output folder')

parser.add_argument('--head', dest='head_row', action=argparse.BooleanOptionalAction,
                    help='with or without column names, default value: True')

args = parser.parse_args()


def divide_chunks(rows: List[str], slice_factor: int) -> Generator:
    for i in range(0, len(rows), slice_factor):
        yield rows[i:i + slice_factor]


def csv_divider(input_file: str, lines: int, output_path: str = None, head_row: bool = True):
    folder_name = os.path.basename(input_file).split(".")[0]
    if output_path is None:
        output_path = os.path.join(os.path.dirname(input_file), folder_name)

    # create output path if not exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(f'Opening input_file {input_file}')
    csv_file = open(input_file, 'r', encoding="utf-8")
    head = csv_file.readline() if head_row is True else ''

    print('Reading input_file...')
    txt = csv_file.read().split('\n')[1:]

    print(f"Writing data in files as below:")
    for index, sub in enumerate(divide_chunks(txt, lines)):
        path = os.path.join(output_path, f"{folder_name}_{index}.csv")
        with open(path, 'w') as sub_file:
            sub_file.write(head)
            sub_file.writelines([s + '\n' for s in sub])
        print(path)


def main():
    csv_divider(**vars(args))


if __name__ == '__main__':
    main()
