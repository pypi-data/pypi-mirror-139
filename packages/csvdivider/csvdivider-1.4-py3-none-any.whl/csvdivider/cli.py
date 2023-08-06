import argparse
from .csv_divider import csv_divider


def main():
    parser = argparse.ArgumentParser(description='Dividing CSV into separated CSVs.')

    parser.add_argument('lines', type=int,  required=True,
                        help='Insert a column of line numbers at the front of the output.')

    parser.add_argument('-i', '--input_file', dest='input_file',  required=True,
                        help='The CSV file to operate on. ')

    parser.add_argument('-o', '--output_path', dest='output_path', nargs='?',
                        help='output folder')

    parser.add_argument('--head', dest='head_row', action=argparse.BooleanOptionalAction,
                        help='with or without column names, default value: True')

    args = parser.parse_args()
    csv_divider(**vars(args))
