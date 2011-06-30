.. -*- coding: utf-8 -*-

==================
distwebres package
==================

.. contents::

Introduction
============

distwebres is an extra command for distutils/setuptools/distribute that allow to
minify and compress a package's javascript and CSS resources.

This package can use YUI compressor and Google closure-compiler.

Installation
============

Standard installation with `easy_install` or `pip install`. It is recommended to
install in a virtualenv. The required compilers should be downloaded at install time.

For distwebres development
--------------------------

As with any package you should run `python setup.py develop`, but the first time
you also need to run `python setup.py build_py` to download the required
compilers. (And keep using virtualenv for good practices!)

Please note that `distwebres_yui` and `distwebres_closure` are standard
distutils commands, if you want to add a new compressor for distwebres it can be
done as a separate package!

Commands
========

There is one base command: distwebres.

The other commands are subcommands that launch the different tools. They can be
used directly to test their options.

Usage
=====

Suppose you have the following package layout::

    my.package
    ├── setup.py
    └── my
        └── package
            ├── __init__.py
            └── resources
                ├── css
                │   ├── style-part-1.css
                │   └── style-part-2.css
                └── js
                    ├── widget-date.js
                    ├── active-popup.js
                    └── effects.js

You define which compiler you want to use, and how, by adding `setup.cfg` at the
root of the project::

     [distwebres]
     compressors = distwebres_yui

     [distwebres_yui]
     css-minified = resources/css/style.min.css
     css-sources =
         resources/css/style-part-1.css
         resources/css/style-part-2.css

     js-minified = resources/js/lib.min.js
     js-sources =
         resources/js/widget-date.js
         resources/js/active-popup.js
         resources/js/effects.js

You run it like any other distutils command::

    python setup.py distwebres

This will create a minified CSS file `my/package/resources/css/style.min.css`
and a compressed JS file `my/package/resources/js/lib.min.js`

All sources files must be accessible as package resources, i.e. you obtain the
file path like this::

    from pkg_resources import resource_filename
    css_dir = resource_filename('my.package', 'resources/css')
    effects_fullpathname = resource_filename('my.package', 'resources/js/effects.js')

Options reference
=================

distwebres
----------

  * compressors: list of "compressors" to use. They will be executed in
    order. Thus you could have a first one generating CSS from SASS files, then
    the next would compress this generated CSS

distwebres_yui
--------------

Uses the `YUI compressor <http://developer.yahoo.com/yui/compressor/>`_ to
compress resources.

  * `css-minified`: target filename for CSS minified file
  * `css-sources`: list of CSS files. They are concatenated in order of
    declaration
  * `js-minified`: target filename for JS minified file
  * `js-sources`: list of JS files. They are concatenated in order of
    declaration
  * `compressor-jar`: path to an alternative YUI compressor. You must specify
    the filename, not only the path to its directory!

distwebres_closure
------------------

Uses the `Closure compiler <http://code.google.com/closure/compiler/>`_, meant
to be used for a javascript project based on the `Closure library
<http://code.google.com/closure/library/>`_.

Thought the compiler can be used for general JS minification, currently
`distwebres_closure` restricts its usage for a closure library project.

  * `minified`: target filename for JS minified file
  * `deps`: target filename for your project specific JS dependencies. Normally
    this file is useful during development.
  * `root`: path to the root of closure-library. Like all other resources, it
    must be a package resource. You must include all closure-library (in
    particular distwebres need python files located in `closure/bin/build`
  * `project`: path to the directory of your closure-based JS project
  * `inputs`: list of JS files to pass as `inputs` to the closure-compiler. The
    compiler looks for `goog.provide` and `goog.require` to compute which files
    are needed for generating the `minified` file.
  * `namespaces`: you can specify a list of namespaces to compute dependencies
    for.
  * `output-mode`: `compiled`(default), `script`, `list` (list files taken in
    account)
  * `compiler-flags`: optional flags to pass to closure.jar
  * `compiler-jar`: path to another version. You must specify the jar filename,
    not only the path to its directory!

`inputs` and `namespaces` are cumulative, the compiler will merge namespaces
found in `inputs` files with the one you provide in `namespaces`. You must
specify at least one of the two parameters.
