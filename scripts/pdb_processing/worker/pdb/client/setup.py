
#
# Copyright 2017 University of Southern California
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
#

from setuptools import setup

setup(
    name="pdb_workflow_processing_client",
    description="Script for pdb workflow processing",
    version="0.1.1",
    scripts=[
        "pdb_workflow_processing.py",
    ],
    requires=["pdb_workflow_processing_lib"],
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
