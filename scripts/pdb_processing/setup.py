
#
# Copyright 2020 University of Southern California
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
#

from setuptools import setup

setup(
    name="PDB WORKFLOW",
    description="PDB WORKFLOW PROCESSING",
    version="0.1.1",
    scripts=[
        "bin/pdb_worker"
    ],
    requires=['os',
        'sys',
        'logging',
        'deriva'],
    maintainer_email="support@misd.isi.edu",
    license='(new) BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
    ])
