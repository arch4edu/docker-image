#!/bin/python
import sys
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
force['jbig'] = 'jbigkit'
force['jinja2'] = 'python-jinja'
force['jpeg'] = 'libjpeg-turbo'
force['jupyter'] = 'jupyter'
force['jupyter_console'] = 'jupyter_console'
force['jupyterlab'] = 'jupyterlab'
force['jupyterlab_server'] = 'jupyterlab_server'
force['ld_impl_linux-64'] = 'binutils'
force['libgcc-ng'] = 'gcc-libs'
force['libspatialindex'] = 'spatialindex'
force['libuuid'] = 'libutil-linux'
force['lz4-c'] = 'lz4'
force['matplotlib-base'] = 'python-matplotlib'
force['mkl'] = 'intel-mkl'
force['mkl_fft'] = 'python-mkl-fft'
force['mkl_random'] = 'python-mkl-random'
force['msgpack-python'] = 'python-msgpack'
force['nbconvert'] = 'jupyter-nbconvert'
force['nbformat'] = 'jupyter-nbformat'
force['notebook'] = 'jupyter-notebook'
force['numpy-base'] = 'python-numpy-mkl'
force['pandoc'] = 'pandoc'
force['path.py'] = 'python-path'
force['py-lief'] = 'lief'
force['pyyaml'] = 'python-yaml'
force['pyqt'] = 'python-pyqt5'
force['qt'] = 'qt5-base'
force['ruamel_yaml'] = 'python-ruamel-yaml'
force['scipy'] = 'python-scipy-mkl'
force['spyder'] = 'spyder'
force['tbb'] = 'intel-tbb'
force['widgetsnbextension'] = 'jupyter-widgetsnbextension'
force['yaml'] = 'libyaml'

ignore = []
ignore.append('_ipyw_jlab_nb_ext_conf') # anaconda related
ignore.append('_libgcc_mutex') # empty
ignore.append('anaconda') # anaconda related
ignore.append('anaconda-client') # anaconda related
ignore.append('anaconda-navigator') # anaconda related
ignore.append('anaconda-project') # anaconda related
ignore.append('backcall') # already provided by ipython
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

from pyalpm import Handle
arch = 'x86_64'
package = 'jre8-openjdk'
dbpath = '/var/lib/pacman/'
handle = Handle('/', dbpath)
for i in ['core', 'extra', 'community', 'arch4edu']:
    handle.register_syncdb(i, 0)

def check(package):

    for repo in handle.get_syncdbs():
        result = repo.get_pkg(package)
        if result:
            return result
    return None

lines = run_cmd(['pacman', '-Flq', 'anaconda'], silent=True).split('\n')
lines = [line for line in lines if line.startswith('opt/anaconda/conda-meta/') and line.endswith('.json')]
lines = [line[len('opt/anaconda/conda-meta/'):] for line in lines]
output = []
failed = False

for line in lines:
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

    # Ignored all backports for python3
    if pkgver[1].startswith('py') and not package.startswith('python') and package.startswith('backports'):
        output.append('# ignored %s' % '-'.join(line))
        continue

    if pkgver[1].startswith('py') and not package.startswith('python') and check('python-%s' % package):
        output.append('python-%s' % package)
        continue

    if pkgver[1].startswith('py') and check(package):
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
