from setuptools import setup, Extension

verthashsources = [
	'h2.c',
    'tiny_sha3/sha3.c'
]

verthashincludes = [
	'.', 
	'./tiny_sha3'
]

verthash_module = Extension('verthash_test',
                            sources=verthashsources+['verthashmodule.c'],
                            extra_compile_args=['-std=c99'],
                            include_dirs=verthashincludes)

setup(name = 'verthash_test',
      version = '0.0.3',
      author_email = 'vertion@protonmail.com',
      author = 'vertion',
      url = 'https://github.com/vertiond/verthash-pospace',
      description = 'Python bindings for Verthash proof of work function',
      long_description = 'This release supports reading the verthash datafile from disk only',
      ext_modules = [verthash_module])
