# Based on https://gist.github.com/Willy-JL/3eaa171144b3bb0a4602c7b537f90036

import datetime
import os
import re
import sys
from contextlib import contextmanager

# Initialize standard streams
for stream in ("stdout", "stderr", "stdin"):
    if getattr(sys, stream) is None:
        setattr(sys, stream, open(os.devnull, "w+"))

# Save original streams
_stdout = sys.stdout
_stderr = sys.stderr
_stdin = sys.stdin

# Flag to pause file output
_pause_file_output = False

# Get current date and time
now = datetime.datetime.now()
date_time = now.strftime("%d%m%Y_%H%M%S")


# Function to write message to file
def _file_write(message, no_color=True):
    # If output is paused, do nothing
    if _pause_file_output:
        return
    # Remove color codes if no_color is True
    if no_color:
        message = re.sub("\\x1b\[38;2;\d\d?\d?;\d\d?\d?;\d\d?\d?m", "", message)
        message = re.sub("\\x1b\[\d\d?\d?m", "", message)
    # Open log file in append mode and write message
    with open(f"logs/log_{date_time}.txt", "a", encoding="utf-8") as log:
        log.write(message)


# Override classes for stdout, stderr, and stdin
class __stdout_override():
    def write(self, message):
        _stdout.write(message)
        _file_write(message)

    def __getattr__(self, name):
        return getattr(_stdout, name)


class __stderr_override():
    def write(self, message):
        _stderr.write(message)
        _file_write(message)

    def __getattr__(self, name):
        return getattr(_stderr, name)


class __stdin_override():
    def readline(self):
        message = _stdin.readline()
        _file_write(message, no_color=False)
        return message

    def __getattr__(self, name):
        if name == "fileno": raise AttributeError
        return getattr(_stdin, name)


# Context manager to pause file output
@contextmanager
def pause_file_output():
    global _pause_file_output
    _pause_file_output = True
    yield
    _pause_file_output = False


# Function to install the logger
def install():
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")
    # Set system streams to override classes
    sys.stdout = __stdout_override()
    sys.stderr = __stderr_override()
    sys.stdin = __stdin_override()
