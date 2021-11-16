##
# File:    testGetUcode.py
# Date:    15-Nov-2021
# Version: 0.001
##
"""
Tests case for using the Dictionary Api to get all data items of type ucode. 

"""
from __future__ import absolute_import, print_function

import json
import logging
import os
import sys
import time
import unittest

from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import CifName
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter

dictionaryName = sys.argv[1]

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

try:
    from mmcif import __version__
except ImportError:
    sys.path.insert(0, TOPDIR)
    from mmcif import __version__


__docformat__ = "restructuredtext en"
__license__ = "Apache 2.0"


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class DictionaryApiTests(unittest.TestCase):
    def setUp(self):
        self.__lfh = sys.stderr
        self.__verbose = False
        #self.__pathPdbxDictionary = os.path.join(HERE, "data", "ihm-extension.dic")
        self.__pathPdbxDictionary = os.path.join(HERE, dictionaryName)
        self.__containerList = None
        self.__startTime = time.time()
        #logger.debug("Running tests on version %s", __version__)
        #logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def tearDown(self):
        endTime = time.time()
        #logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testGetUcode(self):
        """Test case - Get all data items of type ucode
        """
        print("\n")

        try:
            myIo = IoAdapter(raiseExceptions=True)
            self.__containerList = myIo.readFile(inputFilePath=self.__pathPdbxDictionary)
            dApi = DictionaryApi(containerList=self.__containerList, consolidate=True, verbose=self.__verbose)

            logger.debug("+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
            catNameList = dApi.getCategoryList()
            for catName in catNameList:
                itemNameList = dApi.getItemNameList(catName)
                for itemName in itemNameList:
                    categoryName = CifName.categoryPart(itemName)
                    attributeName = CifName.attributePart(itemName)
                    code = dApi.getTypeCode(categoryName, attributeName)
                    if (code == "ucode"):
                        print("Table: ", categoryName, "\tColumn: ", attributeName, "\tType: ", code)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

def suiteDictionaryApiTests():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(DictionaryApiTests("testGetUcode"))
    return suiteSelect

if __name__ == "__main__":
    mySuite = suiteDictionaryApiTests()
    unittest.TextTestRunner(verbosity=2).run(mySuite)

