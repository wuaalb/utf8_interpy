import os, sys

try:
    from setuptools import setup
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install as _install


def _post_install(install_lib):
    import shutil
    shutil.copy('utf8_interpy.pth', install_lib)

class install(_install):
    def run(self):
        self.path_file = 'utf8_interpy'
        _install.run(self)
        self.execute(_post_install, (self.install_lib,), msg='Running post install task')

version = '1.0'

setup(
    cmdclass={'install': install},
    name='utf8_interpy',
    version=version,
    download_url='git@github.com:wuaalb/utf8_interpy.git',
    packages = ['utf8_interpy'],
    author='Merlijn Blaauw',
    author_email='merlijn.blaauw@gmail.com',
    url='http://github.com/wuaalb/utf8_interpy',
    license='MIT',
    description='Powerful Ruby like string interpolation for Python #{}.',
    long_description=open('README.rst').read(),
    keywords='python string interpolation interpolate ruby codec encoding',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
