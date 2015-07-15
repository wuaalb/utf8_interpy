
Powerful Python String Interpolation
====================================

The *utf8_interpy* package extends Python to support 
much more powerful, *Ruby like* string interpolation **#{}**.

It is a reimplementation of the excellent `interpy`_ package by Syrus Akbary, 
which was in turn inspired by the Dropbox `pyxl template engine`_.

Examples
--------

All Python source files which start with a 'utf8-interpy' encoding cookie will allow using Ruby like string interpolation.

.. code:: python

    # coding: utf8-interpy
	
Now any Python expression within **#{..}** inside a double quoted string will be interpolated. That is, the expression will be evaluated, converted to a text string and embedded in the outer string.

A simple example would be,

.. code:: python

	your_name = 'John'
	print("Hello #{your_name}")

One use might be creating complex yet highly readable path strings, e.g.

.. code:: python
	
	datdir = '/projects/data'
	ver = 1
	feat = 'spe'
	ndim = {'mfc' : 35, 'spe' : 513}
	search = "#{datdir}/feat/#{feat}_#{ndim[feat]}/ver#{ver}/*.#{feat}"
	
Or, performing small operations *inline* when calling external command line applications, e.g.

.. code:: python

	cmd = "calc_mfc --order #{ndim['mfc']-1} #{in_wav} #{out_mfc}"

You can freely interpolate local and global variables, e.g.

.. code:: python

	global_var = 'foo'
	
	def my_fun():
		local_var = 'bar'
		print("#{global_var}#{local_var}")
		
Many of such things would require much more verbose and hard to read syntax when using standard Python interpolation, e.g.

.. code:: python

	print("Hello %s" % (your_name))
	print("Hello {}".format(your_name))
	print("Hello {your_name}".format(your_name=your_name))
	print("Hello {your_name}".format(**locals()))
	
	search = "{}/feat/{}_{}/ver{}/*.{}".format(datdir, feat, ndim[feat], ver, feat)
	search = "{datdir}/feat/{feat}_{ndim}/ver{ver}/*.{feat}".format(datdir=datdir, feat=feat, ndim=ndim[feat], ver=ver)
	search = os.path.join(datdir, feat, '%s_%d' % (feat, ndim[feat]), 'ver%d' % ver, '*.%s' % feat)
	
	print("#{global_var}#{local_var}".format(global_var=global_var, local_var=local_var))
	print("#{global_var}#{local_var}".format(**dict(globals(), **locals())))
	
Installation
------------

The installation of this package is quite simple, you only have to run

	``pip install utf8_interpy``

Or locally, from the downloaded zip file, run

	``pip install utf8_interpy-master.zip``
	
You can also use utf8_interpy without global installation, just use

.. code:: python
	
	import utf8_interpy.codec
	
From the entry point of your application (which will register the codec), before importing any modules using utf8_interpy.
It is not possible to register the codec from the .py file which uses utf8_interpy itself; if the entry point requires interpolation, write a little wrapper .py file which registers the codec and then runs the main entry point.	
	
How it works
------------

When executing or importing a .py file, the interpreter first tries to determine its decoding by looking for a '# coding: xyz' cookie in the first two lines of the file. Then it will use the codec corresponding to that encoding to decode the byte data into Unicode data before interpreting it (see `PEP 263`_).

The special 'utf8-interpy' encoding is a *wrapper* around the standard 'utf-8' encoding that performs some additional *pre-processing* of source code files encoded at UTF-8 (*without* BOM signature).

This pre-processing converts code like 

.. code:: python

	print("Hello #{your_name}")
	
to

.. code:: python

	print(("Hello "+str(your_name)+""))
	
As all of this is done as a pre-processing step, it adds little run-time overhead to your code, and does not require wrapping strings in special interpolation functions.

Isn't this abusing Python's encoding mechanism?
-----------------------------------------------

Maybe a little.

However,

1. it is just a *lightweight wrapper* around the 'utf-8' codec, 
2. all the heavy lifting in the pre-processor relies on the *tokenize module* in the Python standard library, and 
3. the extended syntax is *limited to string literals* only, not code itself.

So overall, using this package should be relatively safe.

Why use Ruby like syntax
------------------------

While seemingly strange, using Ruby like syntax within Python has a number of advantages

- Syntax is similar to Python's existing string interpolation syntax, {} vs. #{}.
- However, it is not is not exactly the same, meaning *it can be used in combination with standard Python string interpolation*, which has additional formatting options.
- Existing code using standard Python string interpolation *will continue to work as expected*.
- There is a *clear distinction* between interpy and standard string interpolation.
- Requiring double quotes (not single quotes) *offers a mechanism to completely bypass interpy* string interpolation.
- It is an existing standard, although "#@var #@@var #$var" syntax for instance, class and global variables respectively, is not supported.

Known issues
------------

- Using interpy string interpolating from within REPL and interactive debuggers is a bit of a hassle; see below.

- PTVS (2.1, 2.2RC) gives errors such as "Error	1	encoding problem: unknown encoding (line 1)	foobar.py	1	11"; these can safely be ignored.

- PTVS (2.1, 2.2RC) fails to properly save files that use both Unicode characters and a '# coding: utf8-interpy' cookie; try avoid using both at the same time, or use an external editor.

- Source file encoding cannot contain a UTF-8 BOM; this is a limitation of Python (UTF-8 BOM is only allowed with 'utf-8-sig' cookie).


Interpolating strings from REPL and interactive debuggers
---------------------------------------------------------

Some interactive environments (REPL console, debuggers) do not allow setting the encoding used; however we can define a helper function _s() to allow string interpolation in interactive environments.

.. code:: python

	from utf8_interpy.codec import transform_bytes_string; _s = lambda input: eval(transform_bytes_string(b'"' + input.encode('utf-8') + b'"'))
	
Afterwards we can use it to do interactive interpolations

.. code:: python

	>>> test = 'foobar'
	>>> _s("#{test}")
	'foobar'
	
Compatibility with editors
--------------------------

Certain editors will not be able to determine the actual encoding of the .py files to be UTF-8.
This may cause Unicode characters in the source code to be replaced or displayed incorrectly.

Unfortunately it doesn't seem possible use the 'utf-8-sig' encoding as a base encoding for the wrapper and let the BOM signature indicate the encoding to editors.

Compatibility with code analyzers
---------------------------------

Code analyzers such as Pylint should work as expected, as long as they use the Python codecs to load the file (and utf8_interpy is installed globally).

Differences from original interpy package
-----------------------------------------

While *utf8_interpy* follows the same implementation as the original *interpy* package, it was rewritten from scratch to make it more robust to edge cases that can happen in larger scripts.

- Uses the tokenize module to untokenize, ensuring that round-trip preprocessing maintains same line numbers. This caused the original interpy to break PTVS debugger for some edge cases.

- Does not pre-process docstrings and raw strings.

- Handles a number of edge cases better (e.g. string concatenations without + operator, combination of interpy and Python interpolation, ...).

- Pre-processing tries to avoid throwing exceptions, instead it just lets the input pass through unprocessed.
  The idea behind this is that in case there are any syntax errors, indentation errors, etc. in the source code we don't want this to cause an exception in the encoding codec because it causes unfamiliar and in Py2's case uninformative error messages to the user.
  Instead, we just let the interpreter handle it, which either causes a familiar error message or in the worst case causes string literals to be different than expected.

- Instead of using the tokenize.generate_tokens() method (which is exists but is undocumented for Py3), tries to wrap Py2 version of the tokenize module to make it roughly equivalent to Py3 tokenize module.

- Removes dependency on the *six* Py2/Py3 compatibility module. However, this makes it less compatible with older versions of Python (pre-2.7, pre-3.4).

- Adds a bunch of unit tests.

Compatibility
-------------

This package is compatible with modern versions of Python, i.e. 2.7.x and 3.4+.

.. _interpy: https://github.com/syrusakbary/interpy
.. _pyxl template engine: https://github.com/dropbox/pyxl
.. _PEP 263: http://www.python.org/dev/peps/pep-0263/

