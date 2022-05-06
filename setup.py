"""
@Author = 'Mike Stanley'

Describe this file.

============ Change Log ============
10/2/2020 = Created.

============ License ============
Copyright (C) 2020 Michael Stanley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from setuptools import setup, find_packages

setup(
    name='wmul_test_utils',
    version='0.1.0',
    license='GPLv2',
    description="'Various utilities for testing WMUL-FM's other packages.",

    author='Michael Stanley',
    author_email='stanley50@marshall.edu',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[],
    tests_require=["pytest", "pyfakefs", "pytest-mock"],
    test_suite="tests"
)
