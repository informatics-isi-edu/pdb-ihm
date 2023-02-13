#
# Copyright 2020 University of Southern California
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from setuptools import setup, find_packages

url = "https://github.com/informatics-isi-edu/protein-database"
author = 'USC Information Sciences Institute, Informatics Systems Research Division'
author_email = 'isrd-support@isi.edu'

setup(
    name='pdb_dev',
    description='PDB-Dev python module',
    version='1.0',
    url=url,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    packages=find_packages(exclude=["tests", "tmp"]),
    entry_points={
        'console_scripts': [
            'pdb_dev_clear_entry_record = smite.tools.clear_entry_record:main',
#            'smite-imaging-client = smite.pipelines.image_processing.client:main'
        ]
    },
    # move all image processing to requires if downloading lots of dependencies is a concern. 
    install_requires=[
        'deriva',
    ],
    license='Apache 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',        
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
