import asyncio
import time


def make2digit(num: str):
    while len(num) < 2:
        num = "0" + num
    return num


def get_time():
    the_time = time.localtime(time.time())
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    return make2digit(str(the_time.tm_mday)) + " " + months[the_time.tm_mon - 2] + " " + make2digit(
        str(the_time.tm_year)) + " " + make2digit(str(the_time.tm_hour)) + ":" + make2digit(
        str(the_time.tm_min)) + ":" + make2digit(str(the_time.tm_sec))


class Clock:
    def __init__(self):
        self._private_start = time.time()
        self.thr = asyncio.run(self._private_fps_count())
        self._private_f = 0
        self._private_new_f = 0
        self._private_t = [self._private_start, self._private_start]

    def tick(self, fps: int) -> float:
        """Tick clock and return ms waited float"""
        x = time.time()
        self._private_t.pop(0)
        self._private_t.append(x)
        p = (1 / fps) - (x - self._private_start)
        if p > 0:
            time.sleep(p)
        self._private_f += 1
        self._private_start = time.time()
        return p * 1000.0

    async def _private_fps_count(self):
        while True:
            await time.sleep(1)
            self._private_new_f = self._private_f
            self._private_f = 0

    def get_fps(self) -> int:
        """Gets FPS."""
        return self._private_new_f

    def get_time(self) -> float:
        """Return float of ms between the last 2 calls of tick()"""
        return (self._private_t[1] - self._private_t[0]) * 1000.0