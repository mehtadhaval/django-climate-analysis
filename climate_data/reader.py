import contextlib

from django.conf import settings


class ClimateDataFileReader(object):

    skip_lines = settings.MET_DATA_SKIP_LINES

    def __init__(self, file_name):
        self._file_name = file_name

    def __enter__(self):
        self._file = open(self._file_name, mode='r')
        for index in range(0, self.skip_lines):
            self._file.readline()
        self._header = self._file.readline().lower().split()
        return self

    def __iter__(self):
        return self

    def __next__(self):
        next_line = self._file.readline()
        if not next_line:
            raise StopIteration
        return dict(zip(self._header, next_line.split()))

    def __exit__(self, *args, **kwargs):
        if not self._file:
            return
        with contextlib.suppress(Exception):
            self._file.close()
