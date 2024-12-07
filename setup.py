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

from setuptools import setup, find_namespace_packages

url = "https://github.com/informatics-isi-edu/pdb-ihm"
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
    keywords=['pdb_dev', 'ihm', 'protein structure'],
    packages=find_namespace_packages(exclude=["tests", "tmp"]),
    entry_points={
        'console_scripts': [
            'pdb_dev_clear_entry_record = pdb_dev.tools.clear_entry_record:main',
            'pdb_process_entry = pdb_dev.processing.curation.pdb_process_entry:main',
            'pdb_curation_worker = pdb_dev.processing.curation.pdb_curation_worker:main',
        ]
    },
    # scripts
    #scripts=['pdb_dev/processing/curation/pdb_worker'],
    # move all image processing to requires if downloading lots of dependencies is a concern. 
    install_requires=[
        'deriva',
        'deriva-extras',
    ],
    # packages that are properly arranged with setuptools, but aren't published to PyPI
    #dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
    #
    # include non-code data in the distribution specified in MANIFEST.in
    #include_package_data=True,
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
