import unittest
from PIL import Image, ImageTk

import sys
sys.path.append('../src/TestCase')
sys.path.append('../src')
sys.path.append('../src/Save')
from Executor import Executor
from TestStep import Step
from TestCase import TestCase

class ExecutorActionTestSuite(unittest.TestCase):
    def testExecuteClick(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Click', val=Image.open('./TestCase/Test/image/exist.png'))
        exe.execute(0)
        self.assertEqual('Success', exe.execute(1))
        exe.execute(0)
    def testExecuteClickNotFound(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Click', val=Image.open('./TestCase/Test/image/notexist.png'))
        exe.execute(0)
        self.assertEqual('Failed', exe.execute(1))

    def testExecuteSetText(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='TestCase', val='./TestCase/SetText/SetTextSetUp')
        case.insert(act='Set Text', val='Hello World')
        case.insert(act='TestCase', val='./TestCase/SetText/SetTextTearDown')
        exe.execute(0)
        self.assertEqual('Success', exe.execute(1))
        target = Image.open('./TestCase/SetText/source.png')
        self.assertEqual('Success', exe.imageFinder(targetImage=target))
        exe.execute(2)

    def testExecuteTestCase(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='TestCase', val='./TestCase/Test')
        self.assertEqual('Success', exe.execute(0))
    def testExecuteTestCaseExcept(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='TestCase', val='D:/')
        self.assertEqual('Error', exe.execute(0))

    def testExecuteAssertExist(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Android Keycode', val='KEYCODE_HOME')
        case.insert(act='Assert Exist', val=Image.open('./TestCase/Test/image/exist.png'))
        exe.execute(0)
        self.assertEqual('Success', exe.execute(1))
        exe.execute(0)
    def testExecuteAssertExistFailed(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Assert Exist', val=Image.open('./TestCase/Test/image/notexist.png'))
        self.assertEqual('Failed', exe.execute(0))

    def testExecuteAssertNotExist(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Assert Not Exist', val=Image.open('./TestCase/Test/image/notexist.png'))
        self.assertEqual('Success', exe.execute(0))
    def testExecuteAssertNotExist(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Assert Not Exist', val=Image.open('./TestCase/Test/image/exist.png'))
        self.assertEqual('Failed', exe.execute(0))

    def testExecuteNestLoop(self):
        case = TestCase()
        exe = Executor(case)
        case.insert(act='Loop Begin', val='2')
        case.insert(act='Sleep(s)', val='0')
        case.insert(act='Loop Begin', val='2')
        case.insert(act='Swipe', val='start x=500, y=1000, end x=300, y=1000')
        case.insert(act='Loop End', val=None)
        case.insert(act='Android Keycode', val = 'KEYCODE_HOME')
        case.insert(act='Loop End', val=None)
        self.assertEqual('Success', exe.execute(0))
