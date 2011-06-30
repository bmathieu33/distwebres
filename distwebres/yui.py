# -*- coding: utf-8 -*-
from __future__ import with_statement # for python 2.5
import tempfile
import subprocess
from pkg_resources import resource_filename
from distutils.cmd import Command
from distutils import log
from distutils.errors import DistutilsError

DEFAULT_JAR = 'resources/yui/yuicompressor.jar'

class yui(Command):
    # Brief (40-50 characters) description of the command
    description = ""

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [
        ('css-minified=', None, 'Minified CSS output filename'),
        ('css-sources=', None, 'CSS sources files'),
        ('compressor-jar=', None, 'path for yuicompressor-x.x.x.jar')
        ]

    def initialize_options(self):
        self.compressor_jar = None
        self.compress_css = False
        self.css_minified = None
        self.css_sources = ""

    def finalize_options(self):
        package_name = self.distribution.metadata.name

        if self.compressor_jar is None:
            self.compressor_jar = resource_filename('distwebres', DEFAULT_JAR)

        self.ensure_filename('compressor_jar')

        if self.css_minified is not None:
            self.css_minified = resource_filename(package_name, self.css_minified)
            self.css_sources = [resource_filename(package_name, src)
                                for src in self.css_sources.split()]
            if self.css_sources:
                self.compress_css = True

    def run(self):
        if self.compress_css:
            self.build_css()

    def build_css(self):
        # concat CSS source in a single temp file
        log.info('Minify CSS resources:')
        with tempfile.NamedTemporaryFile(suffix='.css') as all_sources:
            for filename in self.css_sources:
                all_sources.write(open(filename, 'r').read())
                all_sources.write('\n')
                log.info('   * %s', filename)

            log.info('  => %s', self.css_minified)
            all_sources.seek(0)
            args = ['java',
                    '-jar', self.compressor_jar,
                    '--type', 'css',
                    '-o', self.css_minified,
                    all_sources.name,
                    ]
            proc = subprocess.Popen(args, close_fds=True)
            proc.wait()

            if proc.returncode != 0:
                msg = 'YUI minify CSS failed! command was: "%s"' % ' '.join(args)
                log.error(msg)
                raise DistutilsError, msg
