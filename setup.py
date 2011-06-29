from setuptools import setup, find_packages
import pkg_resources
import os
import urllib2
import zipfile
from cStringIO import StringIO

version = '1.0.0'

try:
    _build_py = pkg_resources.iter_entry_points(
        'distutils.command', 'build_py').next().load()
except StopIteration:
    import setuptools.command.build_py
    _build_py = setuptools.command.build_py.build_py

CLOSURE_URL = 'http://closure-compiler.googlecode.com/files/compiler-latest.zip'
CLOSURE_DIR = os.path.join('resources', 'closure')

class build_py(_build_py):

    def  run(self):
        self.install_resources_compilers()
        _build_py.run(self)

    def find_data_files(self, package, src_dir):
        filenames = _build_py.find_data_files(self, package, src_dir)

        if package == "distwebres":
            from distutils import log
            log.info("adding closure compiler in resources")
            resources_dir = os.path.join(src_dir, 'resources')
            filenames.extend(
                (os.path.join(cur_dir, fname)
                 for cur_dir, ignored, dir_files in os.walk(resources_dir)
                 for fname in dir_files
                 ))

        return filenames

    def install_resources_compilers(self):
        from distutils import log
        base_dir = os.path.join('distwebres', CLOSURE_DIR)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

            log.info("downloading closure compiler from %s" % CLOSURE_URL)
            f = urllib2.urlopen(CLOSURE_URL)
            content = StringIO(f.read())
            f.close()
            content.seek(0)
            zipcontent = zipfile.ZipFile(content, 'r')
            # extract compiler, readme, licence files
            zipcontent.extractall(base_dir)
            assert(os.path.exists(os.path.join(base_dir, 'compiler.jar')))

setup(name='distwebres',
      cmdclass={'build_py': build_py},
      version=version,
      description="Distutils extension to compress JS and CSS files for package distribution",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      package_data={
          '': ['docs/*.txt',],
          },
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=['distribute',],
      entry_points={
          'distutils.commands': [
              'distwebres = distwebres.compress:compress',
              'distwebres_closure = distwebres.closure:closure',
              ],
          },
      )
