"""
This python file contains utility functions regarding files (csv, excel, txt etc...)
"""


def count_row_csv(path):
    f = open(path)
    total = sum(1 for row in f)
    return total-1  # first meta row excludes
