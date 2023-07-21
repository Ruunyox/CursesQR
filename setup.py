from setuptools import setup, find_packages
from setuptools.command.install import install
import os

NAME = 'cursesqr'
VERSION = '0.0'

class InstallScript(install):
    def run(self):
        install.run(self)

def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()

def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

setup(
    name=NAME,
    version=VERSION,
    author="Nick Charron",
    author_email="charron.nicholas.e@gmail.com",
    url='https://github.com/ruunyox/cursesqr',
    license='MIT',
    packages=find_packages(),
    zip_safe=True,
    cmdclass={
        'install': InstallScript
    },
    install_requires=['qrcodegen'],
    entry_points={
        'console_scripts': [
            'cursesqr = cursesqr.bin.cursesqr:__main__',
        ],
    }
    )
