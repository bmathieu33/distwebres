# -*- coding: utf-8 -*-
from distutils.cmd import Command
from distutils import log

class compress(Command):
    # Brief (40-50 characters) description of the command
    description = ("Use externals JS and CSS compressors for package JS/CSS "
                   "resources")

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [('compressors=', None, "compressors to use"),]

    def initialize_options (self):
        self.compressors = ""

    def finalize_options (self):
        self.compressors = self.compressors.split()

    def run (self):
        if not self.compressors:
            log.info('No rule for JS or CSS compression, skipping.')
            return

        for command in self.compressors:
            self.run_command(command)
