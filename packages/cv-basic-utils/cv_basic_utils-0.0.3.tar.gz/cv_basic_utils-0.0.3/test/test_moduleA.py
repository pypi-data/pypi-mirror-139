import cv_basic_utils as mlu

import unittest


class TestModuleA(unittest.TestCase): 
    
    def test_fun_a1(self):
        self.assertTrue(mlu.subpackage1.moduleA.fun_a1())
    
    def test_fun_a2(self):
        self.assertTrue(mlu.subpackage1.moduleA.fun_a2())
    
if __name__ == '__main__':
    unittest.main() 


