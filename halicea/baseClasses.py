import os, shutil
from codeBlocksHelpers import *

from locators import *

class Model(object):
    def __init__(self):
        self.Package = ''
        self.Name = ''
        self.References = []
        self.Properties = []
        self.InheritsFrom = ''
        self.SourceCode = ''
    @property
    def FullName(self):
        return self.Package+'.'+self.Name

class Property(object):
    def __init__(self):
        self.Name = ''
        self.Type = ''
        self.Options = None
        self.Required = 'False'
        self.Default = None

class Package(object):
    def __init__(self, name):
        self.Name =name
        self.SubPackages = []
        self.ModelModules =[]
        self.Views = []
        self.Forms = []
        self.ControllerModules = []
        self.StaticData =[]
        self.JScripts = []
        self.Bases =[]
        self.Blocks = []

    @staticmethod
    def PathFromName(packageFullName):
        return os.path.join(packageFullName.split('.'))
    @staticmethod
    def packPackage(packageList, destination):
        for packageName in packageList:
            vDir = LocatePagesDir(packageName)
            fDir = LocateFormsDir(packageName)
            cModule = LocateControllerModule(packageName)
            mModule = LocateModelModule(packageName)
            shutil.copytree(vDir, pjoin(destination, vDir))
            shutil.copytree(fDir, pjoin(destination, fDir))
            shutil.copy(cModule, pjoin(destination, 'Controllers.py'))
            shutil.copy(mModule, pjoin(destination, 'Models.py'))
         
    def unpackPackage(self, packFile):
        pass

class BlockTypes(object):
    LINE = 1
    BLOCK = 2

class Block(object):
    Parrent = None
    Children = []
    Name = ''
    __Code = ''
    BlockType = BlockTypes.LINE
    __Locator = HalCodeBlockLocator()
    @property
    def LineCount(self):
        if self.BlockType==BlockTypes.LINE:
            return 1
        else:
            if self.Children:
                return sum([x.LineCount for x in self.Children])
            else:
                return 0
    
    @staticmethod
    def createEmptyBlock(name, cbl=HalCodeBlockLocator()):
        return Block.loadFromLines(cbl.createValidBlock(name).split('\n'),'root',cbl)[name]

    @staticmethod
    def loadFromLines(lines, rootName='root', cbl=HalCodeBlockLocator()):
        rt = Block(parrent=None, name=rootName, blType=2)
        blockqueue = [rootName]
        currentBlock = rt
        for line in lines:
            name = cbl.lineIsBlockBegin(line)
            if name:
                newBlock = Block(currentBlock, name, BlockTypes.BLOCK)
                currentBlock.append(newBlock)
                currentBlock = newBlock
                blockqueue.append(name)
            currentBlock.append(Block.createLineBlock(line))
            if cbl.lineIsBlockEnd(line):
                blockqueue.pop()
                currentBlock = rt['.'.join(blockqueue[1:])]
        return rt
    
    def createEmptyBlocks(self, blockName, cbl=HalCodeBlockLocator()):
        parts= blockName.split('.')
        curBlock = self
        for p in parts:
            if not curBlock[p]:
                curBlock.append(Block.createEmptyBlock(p, cbl))
            curBlock = curBlock[p]
    @staticmethod
    def loadFromText(text, cbl=HalCodeBlockLocator(), renderer=None, renderDict={}):
        txt =text
        if renderer:
            txt = renderer(renderDict)
        return Block.loadFromLines(txt.split('\n'), 'root', cbl)
    @staticmethod
    def createLineBlock(line):
        return Block(None, line, blType=BlockTypes.LINE)

    @staticmethod
    def loadFromFile(filePath, cbl=HalCodeBlockLocator(), renderer=None, renderDict={}):
        txt = ''
        if renderer:
            txt = renderer(filePath, renderDict)
        else:
            txt = open(filePath, 'r').read()
        lines = txt.split('\n')
        return Block.loadFromLines(lines, filePath, cbl)
    @staticmethod
    def openOrCreate(filePath, cbl=HalCodeBlockLocator(), renderer=None, renderDict={}, defaultLines=[]):
        if os.path.exists(filePath):
            #we dont need rendering here, we just need a simple fileload.
                return Block.loadFromFile(filePath, cbl, renderer, renderDict)
        else:
            return Block.loadFromLines(defaultLines, 'root', cbl)

    def saveToFile(self, filePath, mode='w'):
        if not os.path.exists(os.path.dirname(filePath)):
            os.makedirs(os.path.dirname(filePath))
        f = open(filePath, mode)
        f.write(str(self))
        f.close()
    def writeToStream(self, outStream):
        outStream.write(str(self))
    def __init__(self, parrent, name, blType=1):
        self.Parrent = parrent
        self.Children = []
        self.Name = name
        self.BlockType = blType

    def remove(self, element):
        self.Children.remove(element)

    def pop(self):
        return self.Children.pop()

    def append(self, element):
        if isinstance(element, Block):
            element.Parrent = self
            if len(self.Children)>1: 
                cnt = len(self.Children)-1
                if self.Children[cnt].BlockType==BlockTypes.LINE and \
                   self.__Locator.lineIsBlockEnd(str(self.Children[cnt])) and \
                   self.__Locator.lineIsBlockBegin(str(self.Children[0])):
                    self.Children.insert(cnt, element)
                else:
                    self.Children.append(element)
            else:
                self.Children.append(element)
        else:
            raise Exception('Invalid object passed')
    def appendLines(self, lines=[]):
        for line in lines:
            self.append(Block.createLineBlock(line))
    def appendText(self, text):
        self.appendLines(text.split('\n'))
    def insert(self, index, element):
        if isinstance(element, Block):
            element.Parrent = self
            self.Children.insert(index, element)
        else:
            raise Exception('Invalid object passed')
        
    def __getitem__(self, name):
        if not name:
            return self
        parts = name.split('.'); parts.reverse()
        if len(parts)>1:
            p = self[parts[-1]]
            if p:
                return p['.'.join(parts[:-1])]
        else:
            for child in self.Children:
                if child.Name == parts[0]:
                    return child
        return None

    def __iter__(self):
        return self.Children

    def __str__(self):
        if self.BlockType == BlockTypes.LINE:
            return self.Name
        else:
            items = []
            for t in self.__iter__():
                items.append(t.__str__())
            return '\n'.join(items)
