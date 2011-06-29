# -*- coding: utf-8 -*-
import os
import sys
from pkg_resources import resource_filename
from distutils.cmd import Command
from distutils.errors import DistutilsOptionError

class closure(Command):
    # Brief (40-50 characters) description of the command
    description = ""

    # List of option tuples: long name, short name (None if no short
    # name), and help string.
    user_options = [
        ('root', None, 'closure-library root directory'),
        ('project', None, 'main JS project directory'),
        ('deps', None, 'JS dependency generated file for project'),
        ('minified', None, 'minified JS file to generate'),
        ('inputs', None, 'additionnal JS input directories'),
        ('namespaces', None, ('declared namespaces to take in account '
                              'for minification')),
        ]

    def initialize_options(self):
        self.root = None
        self.project = None
        self.deps = None
        self.minified = None
        self.inputs = ""
        self.namespaces = None

    def finalize_options(self):
        is_dir = self.ensure_dirname
        is_file = self.ensure_filename
        package_name = self.distribution.metadata.name

        for name, validate in (('root', is_dir) ,
                                ('project', is_dir),
                                ('deps', is_file),
                                ('minified', is_file)):
            val = resource_filename(package_name, getattr(self, name))
            setattr(self, name, val)
            validate(name)

        self.ensure_string_list('inputs')
        self.inputs = [resource_filename(package_name, dirname)
                       for dirname in self.inputs]
        for dirname in self.inputs:
            if not os.path.isdir(dirname):
                raise (DistutilsOptionError,
                       ("error in 'inputs' option: %s does not exists or is "
                        "not a directory") % (val,))

        closure_tools_path = os.path.join(self.root, 'closure', 'bin', 'build')
        sys.path.append(closure_tools_path)
        try:
            import closurebuilder
        except ImportError:
            raise DistutilsOptionError, (
                   "root=%s is not the root of closure library: cannot find "
                   "closurebuilder.py in %s" % (self.root, closure_tools_path))

    def run (self):
        from distutils import log
        log.info("options: %s", self.root)
