import json
import os
from tkinter import filedialog
from PIL import Image
import Mouse

from TestCaseUI import TestCaseUI
from TestStep import Step

class SaveFile:
    def saveButtonClick(self, event=None):
        self.saveFile()

    def saveFile(self):
        self.getSaveFilePath()
        self.getFolderName()
        if self._filePath == '': return
        self.jsonEncoder()

    def getSaveFilePath(self):
        _f = filedialog.asksaveasfilename(title="Save as...", filetypes=[("TestCase JSON Files", "*.json")])
        if not _f is '':
            if '.json' not in _f:
                _f = _f + '.json'
            self._filePath = _f
            self._fileName = _f.split('/').pop().rstrip('.json')

    def jsonEncoder(self):
        _dataDict = {}
        _case = TestCaseUI.getTestCaseUI().ctrl.case
        for i in range(_case.getSize()):
            _data = {}
            act = _case.getSteps(i).getAction()
            _data['action'] = act
            if str(_case.getSteps(i).getValue().__class__) == "<class 'PIL.PngImagePlugin.PngImageFile'>":
                # Image path format: /*TestCaseName*_image/image_*StepNumber*.png
                _imgpath = self._fileName + "_image/image_" + str(i + 1) + ".png"
                if not os.path.isdir(self._folderPath + self._fileName + "_image"):
                    os.makedirs(self._folderPath + self._fileName + "_image")
                _case.getSteps(i).getValue().save(self._folderPath + _imgpath)
                _data['value'] = None
                _data['image'] = _imgpath
            else:
                val = _case.getSteps(i).getValue()
                _data['value'] = val
                _data['image'] = None

            _dataDict[str(i + 1)] = _data

        with open(self._filePath, 'w', encoding='utf-8') as fp:
            json.dump(_dataDict, fp, indent=2)

class LoadFile:
    def loadButtonClick(self, event=None):
        self.loadFile()
        TestCaseUI.getTestCaseUI().reloadTestCaseUI()

    def loadFile(self):
        self.getLoadFilePath()
        self.getFolderName()
        if self._filePath is None or self._filePath is "": return
        self.jsonDecoder()

    def getLoadFilePath(self):
        self._filePath = ""
        _f = filedialog.askopenfile(title="Select File", filetypes=[("TestCase JSON Files", "*.json")])
        if _f is None: return
        self._filePath = _f.name
        self._fileName = _f.name.split('/').pop()

    def jsonDecoder(self):
        with open(self._filePath, 'r') as f:
            dataDic = json.load(f)
        self.case = self.getTestCase()
        self.case.clear()

        for i in range(len(dataDic)):
            data = dataDic[str(i + 1)]

            act = data['action']
            val = data['value']
            if val is None:
                val = Image.open(self._folderPath + data['image'])

            step = Step(act, val)
            self.case.insert(step=step)

    def getTestCase(self):
        return TestCaseUI.getTestCaseUI().ctrl.case

class FileLoader(SaveFile, LoadFile):
    __single = None

    def __init__(self):
        if FileLoader.__single:
            raise FileLoader.__single
        FileLoader.__single = self
        self._filePath = ""
        self._folderPath = ""
        self._fileName = ""
        self.case = None

    def getFileLoader():
        if FileLoader.__single is None:
            FileLoader.__single = FileLoader()
        return FileLoader.__single

    def getFolderName(self):
        _fp = self._filePath
        self._folderPath = _fp.rstrip(self._fileName + '.json')
