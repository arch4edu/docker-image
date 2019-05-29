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
force['importlib_metadata'] = 'python-importlib-metadata'
force['intel-openmp'] = 'intel-openmp'
force['ipython'] = 'ipython'
force['jinja2'] = 'python-jinja'
force['jupyter'] = 'jupyter'
force['jupyter_console'] = 'jupyter_console'
force['jupyterlab'] = 'jupyterlab'
force['jupyterlab_server'] = 'jupyterlab_server'
force['libgcc-ng'] = 'gcc'
force['libgfortran-ng'] = 'gcc-fortran'
force['lz4-c'] = 'lz4'
force['mkl'] = 'intel-mkl'
force['msgpack-python'] = 'python-msgpack'
force['nbconvert'] = 'jupyter-nbconvert'
force['nbformat'] = 'jupyter-nbformat'
force['notebook'] = 'jupyter-notebook'
force['numpy-base'] = 'python-numpy'
force['pyqt'] = 'python-pyqt5'
force['qt'] = 'qt5-base'
force['ruamel_yaml'] = 'python-ruamel-yaml'
force['spyder'] = 'spyder'
force['widgetsnbextension'] = 'jupyter-widgetsnbextension'

ignore = []
ignore.append('_ipyw_jlab_nb_ext_conf')
ignore.append('anaconda')
ignore.append('anaconda-client')
ignore.append('anaconda-navigator')
ignore.append('anaconda-project')
ignore.append('backports')
ignore.append('backports.os')
ignore.append('backports.shutil_get_terminal_size')
ignore.append('conda-build')
ignore.append('conda-env')
ignore.append('conda-verify')
ignore.append('clyent')
ignore.append('distributed')
ignore.append('libcurl')
ignore.append('navigator-updater')
ignore.append('singledispatch')
ignore.append('unicodecsv')

# AUR
ignore.append('astropy')
ignore.append('backcall')
ignore.append('bitarray')
ignore.append('bkcharts')
ignore.append('bokeh')
ignore.append('cytoolz')
ignore.append('dask')
ignore.append('fastcache')
ignore.append('heapdict')
ignore.append('locket')
ignore.append('multipledispatch')
ignore.append('partd')
ignore.append('pep8')
ignore.append('pycrypto')
ignore.append('pytest-arraydiff')
ignore.append('pytest-astropy')
ignore.append('pytest-doctestplus')
ignore.append('pytest-openfiles')
ignore.append('pytest-remotedata')
ignore.append('simplegeneric')
ignore.append('sortedcollections')
ignore.append('toolz')
ignore.append('wurlitzer')
ignore.append('zict')

run_cmd(['sudo', 'pacman', '-Sy'], silent=True)

def check(pkgname):
    try:
        output = run_cmd(['pacman', '-Ssq', pkgname], silent=True)
    except:
        output = ''
    output = output.split('\n')
    if pkgname in output:
        return True
    output = run_cmd(['yay', '-Ssq', pkgname], silent=True)
    output = output.split('\n')
    return pkgname in output

lines = run_cmd(['ls', '/opt/anaconda/conda-meta'], silent=True).split('\n')
output = []

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

    output.append('# failed %s' % '-'.join(line))

with open('packages.txt', 'w') as f:
    f.writelines('\n'.join(output))
    f.flush()
