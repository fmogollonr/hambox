#!/usr/bin/env python
import os
import sys
import threading
import time
import time
import json
import string
import random
import subprocess
import syslog
import logging
import logging.handlers
from urllib.parse import urlparse

try:
    from systemd.journal import JournalHandler
except ImportError:
    from systemd.journal import JournaldLogHandler as JournalHandler
import inspect


class Logger:
    def __init__(self, logname):
        self.log = {}
        self.log = logging.getLogger(logname)
        self.log.addHandler(JournalHandler())

    def send_log(self, logLevel, logMessage):
        if logLevel is "info":
            self.log.setLevel(logging.INFO)
            self.log.info(logMessage)
        elif logLevel is "debug":
            self.log.setLevel(logging.DEBUG)
            self.log.debug(logMessage)
