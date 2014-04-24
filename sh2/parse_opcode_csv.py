# -*- coding: utf-8 -*-
import csv

from sh2.instruction_schema import build_instruction_schema


def load_from_csv(file):
    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            name, _, code = [el.strip() for el in row]
            name = name.strip()
            code = code.strip()
            yield build_instruction_schema(name, code)