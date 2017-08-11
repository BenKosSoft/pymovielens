import sys


class ProgressBar:
    """
    Helper class to create a terminal progress bar
    """

    def __init__(self, total, prefix='', suffix='', decimals=1, bar_length=50, fill='#'):
        """
        Initialize the progressBar
        :param total:      (Required) total iterations, the goal
        :param prefix:     (Optional) prefix string that will show before the progress bar
        :param suffix:     (Optional) suffix string that will show after the progress bar
        :param decimals:   (Optional) positive number of decimals in percent compete
        :param bar_length: (Optional) character length of the progress bar
        :param fill:       (Optional) fill character of the progress bar representing the completed percentage
        """
        self.__completed = 0
        self.__total = float(total)
        self.__prefix = prefix
        self.__suffix = suffix
        self.__decimals = decimals
        self.__bar_length = bar_length
        self.__fill = fill

    # TODO: if prefix is different use different progress bar
    def print_progress(self, progress):
        """
        Update the completed percentage and update the progress bar on the terminal
        :param progress: (Required) amount of progress
        """
        if self.__completed != self.__total:
            # update completed iteration count
            remaining = self.__total - self.__completed
            self.__completed = self.__completed + progress if (progress < remaining) else self.__total

            # create progress bar string and print
            str_format = "{0:." + str(self.__decimals) + "f}"
            percents = str_format.format(100 * self.__completed / self.__total)
            filled_length = int(self.__bar_length * self.__completed // self.__total)
            bar = self.__fill * filled_length + '-' * (self.__bar_length - filled_length)

            sys.stdout.write('\r%s |%s| %s%% %s' % (self.__prefix, bar, percents, self.__suffix))
        else:
            sys.stdout.write('\n')
        sys.stdout.flush()


def _test():
    from time import sleep

    items = list(range(0, 57))
    l = len(items)

    pb = ProgressBar(l, 'Progress', 'Complete')

    for _, _ in enumerate(items):
        sleep(0.25)
        pb.print_progress(1)


if __name__ == '__main__':
    _test()
