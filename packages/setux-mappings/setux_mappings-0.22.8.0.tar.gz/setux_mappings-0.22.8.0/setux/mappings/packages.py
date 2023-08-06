from setux.core.mapping import Packages


class Debian(Packages):
    pkg = dict(
        setuptools = 'python3-setuptools',
        pip        = 'python3-pip',
        venv       = 'python3-venv',
        sqlite     = 'sqlite3',
    )


class FreeBSD_12(Packages):
    pkg = dict(
        setuptools = 'py37-setuptools',
        pip        = 'py37-pip',
        sqlite     = 'sqlite3',
    )


class FreeBSD_13(Packages):
    pkg = dict(
        setuptools = 'py38-setuptools',
        pip        = 'py38-pip',
        sqlite     = 'sqlite3',
    )
