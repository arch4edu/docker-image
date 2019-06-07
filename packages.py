#!/bin/python
import sys
from tqdm import tqdm
from cmd import run_cmd

force = {}
force['alabaster'] = 'python-sphinx-alabaster-theme'
force['ca-certificates'] = 'ca-certificates'
force['cython'] = 'cython'
force['et_xmlfile'] = 'python-et-xmlfile'
force['freetype'] = 'freetype2'
force['glib'] = 'glib2'
force['graphite2'] = 'graphite'
force['importlib_metadata'] = 'python-importlib-metadata'
force['intel-openmp'] = 'intel-openmp'
force['ipython'] = 'ipython'
force['jbig'] = 'jbigkit'
force['jinja2'] = 'python-jinja'
force['jpeg'] = 'libjpeg-turbo'
force['jupyter'] = 'jupyter'
force['jupyter_console'] = 'jupyter_console'
force['jupyterlab'] = 'jupyterlab'
force['jupyterlab_server'] = 'jupyterlab_server'
force['libgcc-ng'] = 'gcc-libs'
force['libuuid'] = 'libutil-linux'
force['lz4-c'] = 'lz4'
force['mkl'] = 'intel-mkl'
force['msgpack-python'] = 'python-msgpack'
force['nbconvert'] = 'jupyter-nbconvert'
force['nbformat'] = 'jupyter-nbformat'
force['notebook'] = 'jupyter-notebook'
force['numpy-base'] = 'python-numpy-mkl'
force['pandoc'] = 'pandoc'
force['py-lief'] = 'lief'
force['pyyaml'] = 'python-yaml'
force['pyqt'] = 'python-pyqt5'
force['qt'] = 'qt5-base'
force['ruamel_yaml'] = 'python-ruamel-yaml'
force['scipy'] = 'python-scipy-mkl'
force['spyder'] = 'spyder'
force['widgetsnbextension'] = 'jupyter-widgetsnbextension'
force['yaml'] = 'libyaml'

ignore = []
ignore.append('_ipyw_jlab_nb_ext_conf') # anaconda related
ignore.append('anaconda') # anaconda related
ignore.append('anaconda-client') # anaconda related
ignore.append('anaconda-navigator') # anaconda related
ignore.append('anaconda-project') # anaconda related
ignore.append('backcall') # already provided by ipython
ignore.append('backports') # not needed for python3
ignore.append('backports.os') # not needed for python3
ignore.append('backports.shutil_get_terminal_size') # not needed for python3
ignore.append('bkcharts') # unmaintained
ignore.append('blas') # empty
ignore.append('conda-build') # anaconda related
ignore.append('conda-env') # anaconda related
ignore.append('conda-verify') # anaconda related
ignore.append('clyent') # not needed for linux
ignore.append('dask-core') # already provided by python-dask
ignore.append('distributed') # should use python-setuptools instead
ignore.append('get_terminal_size') # empty
ignore.append('ipython_genutils') # will be removed
ignore.append('libcurl') # already provided by curl
ignore.append('libgfortran-ng') # already provided by gcc-libs
ignore.append('liblief') # already provided by lief
ignore.append('libstdcxx-ng') # already provided by gcc-libs
ignore.append('navigator-updater') # anaconda related
ignore.append('simplegeneric') # already provided by ipython
ignore.append('singledispatch') # not needed for python3
ignore.append('sphinxcontrib') # empty
ignore.append('unicodecsv') # not needed for python3

# In AUR but not in arch4edu yet
ignore.append('cytoolz')
ignore.append('dask')
ignore.append('heapdict')
ignore.append('partd')
ignore.append('toolz')
ignore.append('zict')

def check(pkgname):
    try:
        output = run_cmd(['pacman', '-Ssq', pkgname], silent=True)
    except:
        output = ''
    output = output.split('\n')
    return pkgname in output

run_cmd(['sudo', 'pacman', '-Sy'])
lines = run_cmd(['ls', '/opt/anaconda/conda-meta'], silent=True).split('\n')
output = []
failed = False

for line in tqdm(lines):
    line = line.split('-')

    if len(line) < 2:
        continue

    package = '-'.join(line[:-2])
    pkgver = line[-2:]
    pkgver[1]

    if package in ignore:
        output.append('# ignored %s' % '-'.join(line))
        continue

    if package in force:
        output.append(force[package])
        continue

    if pkgver[1].startswith('py') and not package.startswith('python') and check('python-%s' % package):
        output.append('python-%s' % package)
        continue

    if pkgver[1].startswith('py') and package.startswith('python') and check(package):
        output.append(package)
        continue

    if pkgver[1].startswith('h') and check(package):
        output.append(package)
        continue

    print('%s failed' % '-'.join(line))
    failed = True

if failed:
    sys.exit(1)

with open('packages.txt', 'w') as f:
    f.writelines('\n'.join(output))
    f.flush()
