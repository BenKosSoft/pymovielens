import csv
import numpy as np
from src import paths

_TEST_RATIO = 0.2


def partition():
    user_dict = {}
    with open(paths.ratings_mini_csv) as ratings:
        csvr = csv.DictReader(ratings, delimiter=',', quotechar='"')
        for row in csvr:
            index = row["userId"]
            value = user_dict.get(index, None)
            if not value:
                user_dict[index] = 1
            else:
                user_dict[index] += 1
    for key in user_dict:
        user_dict[key] = np.round(_TEST_RATIO * user_dict[key])

    with open(paths.ratings_mini_test_csv.format(_TEST_RATIO), 'wb') as r_test:
        with open(paths.ratings_mini_train_csv.format(1 - _TEST_RATIO), 'wb') as r_train:
            with open(paths.ratings_mini_csv) as ratings:
                csvr = csv.DictReader(ratings, delimiter=',', quotechar='"')
                csvw_test = csv.DictWriter(r_test, delimiter=',', quotechar='"', fieldnames=csvr.fieldnames)
                csvw_train = csv.DictWriter(r_train, delimiter=',', quotechar='"', fieldnames=csvr.fieldnames)
                csvw_train.writeheader()
                csvw_test.writeheader()
                for row in csvr:
                    index = row["userId"]
                    if user_dict[index]:
                        user_dict[index] = user_dict[index] - 1
                        csvw_test.writerow(row)
                    else:
                        csvw_train.writerow(row)


if __name__ == '__main__':
    partition()
