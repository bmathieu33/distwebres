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
    description = ("Concatenate and minify JS and CSS resources files with "
                   "YUI compressor")

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [
        ('css-minified=', None, 'Minified CSS output filename'),
        ('css-sources=', None, 'CSS sources files'),
        ('js-minified=', None, 'Minified JS output filename'),
        ('js-sources=', None, 'JS sources files'),
        ('compressor-jar=', None, 'path for yuicompressor-x.x.x.jar'),
        ]

    def initialize_options(self):
        self.compressor_jar = None
        self.compress_css = False
        self.css_minified = None
        self.css_sources = ""
        self.compress_js = False
        self.js_minified = None
        self.js_sources = None

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

        if self.js_minified is not None:
            self.js_minified = resource_filename(package_name, self.js_minified)
            self.js_sources = [resource_filename(package_name, src)
                                for src in self.js_sources.split()]
            if self.js_sources:
                self.compress_js = True



    def run(self):
        if self.compress_css:
            self.build('css')
        if self.compress_js:
            self.build('js')

    def build(self, build_type):
        # concat CSS source in a single temp file
        log.info('Minify CSS resources:')
        minified = getattr(self, '%s_minified' % build_type)
        sources = getattr(self, '%s_sources' % build_type)
        suffix = '.' + build_type

        with tempfile.NamedTemporaryFile(suffix=suffix) as all_sources:
            for filename in sources:
                all_sources.write(open(filename, 'r').read())
                all_sources.write('\n')
                log.info('   * %s', filename)

            log.info('  => %s', minified)
            all_sources.seek(0)
            args = ['java',
                    '-jar', self.compressor_jar,
                    '--type', build_type,
                    '-o', minified,
                    all_sources.name,
                    ]
            proc = subprocess.Popen(args, close_fds=True)
            proc.wait()

            if proc.returncode != 0:
                msg = 'YUI minify CSS failed! command was: "%s"' % ' '.join(args)
                log.error(msg)
                raise DistutilsError, msg
