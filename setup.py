# -*- coding: utf-8 -*-

from ast import parse
from distutils.sysconfig import get_python_lib
from functools import partial
from operator import attrgetter, itemgetter
from os import path
from sys import version_info

from setuptools import find_packages, setup

if version_info[0] == 2:
    from itertools import ifilter as filter
    from itertools import imap as map

if __name__ == "__main__":
    package_name = "healthplatform_stats_rest_api"

    with open(path.join(package_name, "__init__.py")) as f:
        __author__, __version__ = map(
            lambda const: const.value if version_info > (3, 6) else const.s,
            map(
                attrgetter("value"),
                map(
                    itemgetter(0),
                    map(
                        attrgetter("body"),
                        map(
                            parse,
                            filter(
                                lambda line: line.startswith("__version__")
                                or line.startswith("__author__"),
                                f,
                            ),
                        ),
                    ),
                ),
            ),
        )

    to_funcs = lambda *paths: (
        partial(path.join, path.dirname(__file__), package_name, *paths),
        partial(path.join, get_python_lib(prefix=""), package_name, *paths),
    )
    # _data_join, _data_install_dir = to_funcs('_data')

    setup(
        name=package_name,
        author=__author__,
        version=__version__,
        # test_suite=package_name + '.tests',
        packages=find_packages(),
        package_dir={package_name: package_name},
        # data_files=[(_data_install_dir(), map(_data_join, listdir(_data_join())))]
    )
