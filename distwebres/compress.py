# -*- coding: utf-8 -*-
from distutils.cmd import Command

class compress(Command):
    # Brief (40-50 characters) description of the command
    description = ""

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [('compressor=', None, "compressor to use"),]

    def initialize_options (self):
        self.compressor = None

    def finalize_options (self):
        if self.compressor is None:
            raise ValueError, "No compressor defined"

    def run (self):
        self.run_command(self.compressor)
