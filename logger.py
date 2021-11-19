from typing import overload

from coloring import print_color
from modifiableSystems import attributablemethod
from timestuff import get_time


class Logger:
    def __init__(self, logLevel: int = 0, logFile: str = "log.log"):
        self.logFile = logFile
        self.logLevel = logLevel

    @overload
    def trace(self, msg):
        pass

    @overload
    def debug(self, msg):
        pass

    @overload
    def info(self, msg):
        pass

    @overload
    def minorWarn(self, msg):
        pass

    @overload
    def warn(self, msg):
        pass

    @overload
    def minorError(self, msg):
        pass

    @overload
    def error(self, msg):
        pass

    @overload
    def exception(self, msg):
        pass

    @overload
    def crash(self, msg):
        pass

    @attributablemethod(logLevel=-1)
    def trace(self, msg):
        if self.logLevel <= -1:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} TRACE]: {msg}\n")

    @attributablemethod(logLevel=0)
    def debug(self, msg):
        if self.logLevel <= 0:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} DEBUG]: {msg}\n")

    @attributablemethod(logLevel=1)
    def info(self, msg):
        if self.logLevel <= 1:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} INFO]: {msg}\n")

    @attributablemethod(logLevel=2)
    def minorWarn(self, msg):
        if self.logLevel <= 2:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} MINOR_WARN]: {msg}\n")

    @attributablemethod(logLevel=3)
    def warn(self, msg):
        if self.logLevel <= 3:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} WARN]: {msg}\n")

    @attributablemethod(logLevel=4)
    def minorError(self, msg):
        if self.logLevel <= 4:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} MINOR_ERROR]: {msg}\n")

    @attributablemethod(logLevel=5)
    def error(self, msg):
        if self.logLevel <= 5:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} ERROR]: {msg}\n")

    @attributablemethod(logLevel=6)
    def exception(self, msg):
        if self.logLevel <= 6:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} EXCEPTION]: {msg}\n")

    @attributablemethod(logLevel=7)
    def crash(self, msg):
        if self.logLevel <= 7:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} CRASH]: {msg}\n")


class PrintingLogger(Logger):
    @overload
    def trace(self, msg):
        pass

    @overload
    def debug(self, msg):
        pass

    @overload
    def info(self, msg):
        pass

    @overload
    def minorWarn(self, msg):
        pass

    @overload
    def warn(self, msg):
        pass

    @overload
    def minorError(self, msg):
        pass

    @overload
    def error(self, msg):
        pass

    @overload
    def exception(self, msg):
        pass

    @overload
    def crash(self, msg):
        pass

    @attributablemethod(logLevel=-1)
    def trace(self, msg):
        if self.logLevel <= -1:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} TRACE]: {msg}\n")
            print_color(f"[{get_time()} TRACE]: {msg}", 0, 0)

    @attributablemethod(logLevel=0)
    def debug(self, msg):
        if self.logLevel <= 0:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} DEBUG]: {msg}\n")
            print_color(f"[{get_time()} DEBUG]: {msg}", 3, 0)

    @attributablemethod(logLevel=1)
    def info(self, msg):
        if self.logLevel <= 1:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} INFO]: {msg}\n")
            print_color(f"[{get_time()} INFO]: {msg}", 1, 0)

    @attributablemethod(logLevel=2)
    def minorWarn(self, msg):
        if self.logLevel <= 2:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} MINOR_WARN]: {msg}\n")
            print_color(f"[{get_time()} MINOR_WARN]: {msg}", 6, 0)

    @attributablemethod(logLevel=3)
    def warn(self, msg):
        if self.logLevel <= 3:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} WARN]: {msg}\n")
            print_color(f"[{get_time()} WARN]: {msg}", 6, 1)

    @attributablemethod(logLevel=4)
    def minorError(self, msg):
        if self.logLevel <= 4:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} MINOR_ERROR]: {msg}\n")
            print_color(f"[{get_time()} MINOR_ERROR]: {msg}", 4, 0)

    @attributablemethod(logLevel=5)
    def error(self, msg):
        if self.logLevel <= 5:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} ERROR]: {msg}\n")
            print_color(f"[{get_time()} ERROR]: {msg}", 4, 1)

    @attributablemethod(logLevel=6)
    def exception(self, msg):
        if self.logLevel <= 6:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} EXCEPTION]: {msg}\n")
            print_color(f"[{get_time()} EXCEPTION]: {msg}", 4, 3)

    @attributablemethod(logLevel=7)
    def crash(self, msg):
        if self.logLevel <= 7:
            with open(self.logFile, 'a') as fw:
                fw.write(f"[{get_time()} CRASH]: {msg}\n")
            print_color(f"[{get_time()} CRASH]: {msg}", 4, 3)
