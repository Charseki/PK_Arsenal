import time


class calc_time:
    start_time = 0

    def __init__(self):
        self.start_time = time.time()

    def get_diff_time(self):
        now = time.time()
        diff = now - self.start_time
        self.start_time = now
        return diff
