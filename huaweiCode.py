# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 13:50:35 2019

@author: wangyang
"""
# from quene import queue
# global carqueue
import const

const.Maxvalue = 10 ^ 10

# carqueue = queue()
# (道路id，道路长度，最高限速，车道数目，起始点id，终点id，是否双向)
class Road():
    def __init__(self, roadId, length, maxSpeed, laneNum, start, end, dir):
        self.roadId = roadId
        self.length = length
        self.maxSpeed = maxSpeed
        self.laneNum = laneNum
        self.start = start
        self.end = end
        self.dir = dir

    def getDirection(self):
        pass

# (结点id,道路id,道路id,道路id,道路id)
class Cross():
    def __init__(self, crossId, up, right, down, left):
        self.crossId = crossId
        self.up = up
        self.right = right
        self.down = down
        self.left=left

# (车辆id，始发地、目的地、最高速度、出发时间)
class Car():
    def __init__(self, carId, start, end, maxSpeed, startTime):
        self.carId = carId
        self.start = start
        self.end = end
        self.maxSpeed = maxSpeed
        self.startTime = startTime

        self.getEdgeWeight = None
        self.bestWaylist = []  # save RoadId
        self.nowadayRoadID = None
        self.nowadayRoadNeedTime = None
        self.nextRoadID = None
        self.indexNowadayRoadID = None
        self.nowspeed = None

    def updataEdgeWeight(self, catQueue, AdjMax):
        pass

    def bestWay(self):
        pass

    def costTime(self):
        pass


# (建立邻接矩阵）
class creatGraph():
    def __init__(self, nodePath=None, loadPath=None):
        self.nodePath = nodePath
        self.loadPath = loadPath
        self.allLoadDict = {}
        self.allNodeDict = {}

    def __getAllNode(self):
        assert self.allNodeDict is not None, 'the load path is None, plase input correct path'
        with open(self.allNodeDict, 'r') as ftp:
            for line in ftp:
                line = line.replace('(', '').replace(')', '')
                NodeInformation = line.split(',')
                self.allNodeDict[NodeInformation[0]] = Node(NodeInformation[0],
                                                            NodeInformation[1], NodeInformation[2],
                                                            NodeInformation[3], NodeInformation[4])
        return

    def __getAllLoad(self):
        assert self.allLoadDict is not None
        with open(self.allLoadDict, 'r') as ftp:
            for line in ftp:
                line = line.replace('(', '').replace(')', '')
                RoadInformation = line.split(',')
                self.allLoadDict[RoadInformation[0]] = Load(RoadInformation[0],
                                                            RoadInformation[1], RoadInformation[2],
                                                            RoadInformation[3], RoadInformation[4],
                                                            RoadInformation[5], RoadInformation[6])
        return

    def __UnicomNode(self, Node, LoadID, NodeIdList, roadList):
        if self.allLoadDict[LoadID].startNodeID == Node.Id:
            NodeIdList.append(self.allLoadDict[LoadID].endNodeID)
            roadList.append(LoadID)
        elif self.allLoadDict[LoadID].endNodeID == Node.Id and self.allLoadDict[LoadID].Flag:
            NodeIdList.append(self.allLoadDict[LoadID].startNodeID)
            roadList.append(LoadID)

    def __getUnicomNode(self, Node):
        NodeIdList = []
        roadList = []
        NodeIdList = self.__UnicomNode(Node, Node.UpLoadID, NodeIdList, roadList)
        NodeIdList = self.__UnicomNode(Node, Node.RightLoadID, NodeIdList, roadList)
        NodeIdList = self.__UnicomNode(Node, Node.DownLoadID, NodeIdList, roadList)
        NodeIdList = self.__UnicomNode(Node, Node.LeftLoadID, NodeIdList, roadList)

        return NodeIdList, roadList

    def __getAdjacencyMatrix(self):
        AdjMax = {}

        for key in self.allNodeDict:
            AdjMax[key] = {}
            for key2 in self.allNodeDict:
                AdjMax[key][key2] = []

            Node = self.allNodeDict[key]
            NodeIdList, roadIdList = self.__getUnicomNode(Node)
            for NodeID, roadId in zip(NodeIdList, roadIdList):
                AdjMax[key][NodeID].append(roadId)


# 更新每辆车的当前路段，和当前路段需要的时间
class disposeCarQueue():
    def __init__(self, carqueue=None, allLoadDict=None, allNodeDict=None):
        self.carqueue = carqueue
        self.fristUpdataRoadCat = None
        self.allLoadDict = {}
        self.allNodeDict = {}
        self.index = None

    def copy(self):
        newClass = disposeCarQueue()
        newClass.allLoadDict = self.allLoadDict.copy()
        newClass.allNodeDict = self.allNodeDict.copy()
        newClass.carqueue = self.carqueue.copy()
        newClass.fristUpdataRoadCat = self.fristUpdataRoadCat
        newClass.index = self.index
        return newClass

    def __fristUpdataRoadCat(self):
        MinNowRoadcostTime = const.Maxvalue
        index = -1
        for i in range(0, len(self.carqueue)):
            if MinNowRoadcostTime >= self.carqueue[i].nowadayRoadNeedTime:
                MinNowRoadcostTime = self.carqueue[i].nowadayRoadNeedTime
                index = i
        self.index = index
        self.fristUpdataRoadCat = self.carqueue[index]

    def addCat(self, cat):
        self.carqueue.append(cat)
        return

    def __removeCat(self, fisrtCat):
        if fisrtCat.nextRoadID is None:
            del self.carqueue[self.index]
            return True
        return False

    def updataQueue(self):
        for i in range(0, len(self.carqueue)):
            if self.index == i:
                self.__updataFisrtCat(self.carqueue[i])
            else:
                self.__updataOrdinaryCar(self.carqueue[i])

    def __updataOrdinaryCar(self, ordinaryCat):
        ordinaryCat.nowadayRoadNeedTime -= self.carqueue[self.index].nowadayRoadNeedTime

    def __updataFisrtCat(self, fisrtCat):
        if self.__removeCat(fisrtCat):
            fisrtCat.index += 1
            fisrtCat.nowadayRoadID = fisrtCat.bestWaylist[fisrtCat.index]
            self.__updataspeed(fisrtCat)

            if len(fisrtCat.bestWaylist) > fisrtCat.index + 1:
                fisrtCat.nextRoadID = fisrtCat.bestWaylist[fisrtCat.index + 1]
            else:
                fisrtCat.nextRoadID = None

    def __updataspeed(self, Cat):
        MaxTime = self.allLoadDict[Cat.nowadayRoadID].length / ...
        min([self.allLoadDict[Cat.nowadayRoadID].maxspeep, Cat.maxspeed])

        for i in range(0, len(self.carqueue)):
            if i != self.index:
                if Cat.nowadayRoadID == self.carqueue[i].nowadayRoadID:
                    if MaxTime < self.carqueue[i].nowadayRoadNeedTime:
                        MaxTime = self.carqueue[i].nowadayRoadNeedTime

        Cat.nowspeed = self.allLoadDict[Cat.nowadayRoadID].length / MaxTime
        Cat.nowadayRoadNeedTime = MaxTime
