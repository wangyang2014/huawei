# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 13:50:35 2019

@author: wangyang
"""
#from quene import queue 
#global carqueue 
import const 
const.Maxvalue = 10**10
#carqueue = queue()
#(道路id，道路长度，最高限速，车道数目，起始点id，终点id，是否双向)
class edgeInformation():
    def __init__(self,weigh,roadId,lanseNo):
        self.weigh = weigh
        self.roadId = roadId
        self.lanseNo = lanseNo

class Load():
    def __init__(self,Id=None,length=None,maxspeed=None,
                lanseNumber=None,startNode=None,endNode=None,Flag=0):
        self.Id = Id
        self.length = length
        self.maxspeep = maxspeed
        self.lanseNumber = lanseNumber
        self.startNodeID = startNode
        self.endNodeID = endNode
        self.Flag = Flag
        self.direction = self.__getdirection()
        self.lansecatId = {}

    def __getlansecatId(self):
        for i in range(self.lanseNumber):
            self.lansecatId[str(i)] = []

    def __getdirection(self):
        direction = []
        for i in range(self.lanseNumber):
            direction.append(None)
        return direction
        
#(结点id,道路id,道路id,道路id,道路id)        
class Node():
    def __init__(self,idNode,upLoadID,rightLoadID,downLoadID,leftLoadID):
        self.idNode = idNode
        self.upLoadID = upLoad
        self.rightLoadID = rightLoad
        self.downLoadID = downLoad
        self.leftLoadID = leftLoad


#(车辆id，始发地、目的地、最高速度、出发时间)
class cat():
    def __init__(self,Id,startNode,endNode,maxspeed,departureTime):
        self.Id = Id
        self.startNodeID = startNode
        self.endNodeID = endNode
        self.maxspeed = maxspeed
        self.departureTime = departureTime

        self.bestWayList = []      #save RoadId
        self.bestNodeList = []     #save NodeId
        self.bestTurnDirection = [] # save direction
        self.bestCostTime = None
        
        self.weightMat = None #应该存储一个结构{minedge,Load}

        self.getEdgeWeight = None
        
        self.nowadayRoadID = None 
        self.nowadayRoadNeedTime = None
        self.nextRoadID = None
        self.indexNowadayRoadID = None
        self.nowspeed = None
        
    def updataEdgeWeight(self,catQueue,AdjMat):
        self.weightMat = AdjMat.copy()

    
    def bestWay(self,allLoadDict,allNodeDict):#Dijkstra
        sSet = []
        vSet = []
        distance = {}
        forward = {}

        for key in allNodeDict:
            vSet.append(key)
            distance[key] = self.weightMat[self.startNodeID][key].weigh
            forward[key] = self.startNodeID

        sSet.append(self.startNodeID)
        vSet.remove(self.startNodeID)
        forwardNode = self.startNodeID

        while(len(vSet) != 0):
            minvalue = const.Maxvalue
            index = None
            for key in vSet:
                if minvalue > distance[key]:
                    minvalue = distance[key]
                    index = key
            
            #forward[key] = forwardNode
            #forwardNode = key

            sSet.append(index)
            vSet.remove(index)

            for key in vSet:
                if distance[key] > distance[index] + self.weightMat[index][key].weigh:
                    distance[key] = distance[index] + self.weightMat[index][key].weigh
                    forward[key] = index
        
        self.bestCostTime = distance[endNodeID]
        self.__getBestNodeList(forward)
    
    def __getBestNodeList(self,forward):
        nodeId = self.endNodeID
        while(nodeId != self.startNodeID):
            self.bestNodeList.append(nodeId)
            nodeId = forward[nodeId] 
        self.bestNodeList.append(nodeId)
        self.bestNodeList.reverse()

    def __getBestRoadList(self):
        for i in range(0,len(self.bestNodeList) - 1):
            self.bestWayList.append(self.weightMat[self.bestNodeList[i]][self.bestNodeList[i+1]].roadId)

    def __getDirect(self,nodeId,loadId,nowLoadId):
        if nowLoadId is None:
            return 'straight'

        direct = ['left','straight','right']
        turnDict = {'up':{'right':'left','down':'straight','left':'right'},
                    'right':{'up':'right','down':'left','left':'straight'},
                    'down':{'up':'straight','right':'right','left':'left'},
                    'left':{'up':'left','down':'right','left':'right'}}
        
        key1 = self.__getRoaddirect(nodeId,loadId)
        key2 = self.__getRoaddirect(nodeId,nowLoadId)

        return turnDict[key1][key2]

    def __getRoaddirect(self,nodeId,loadId):
        if nodeId.upLoadID == loadId:
            return 'up'
        elif nodeId.rightLoadID == loadId:
            return 'right'
        elif nodeId.downLoadID == loadId:
            return 'down'
        elif nodeId.leftLoadID == loadId:
            return 'left'
        else:
            assert False ,'eeror, the road not have direct' 

    def __getbestTurnDirection(self):
        nowRoadList = self.bestWayList.copy()
        nowRoadList[1:len(nowRoadList)] = self.bestWayList[0:-1]
        nowRoadList[0] = None

        for loadId,nodeId,nowRoadId in zip(self.bestWayList,self.bestNodeList,nowRoadList):
            self.bestTurnDirection.append(self.__getDirect(nodeId,loadId,nowRoadId))


#(建立邻接矩阵）        
class creatGraph():
    def __init__(self,nodePath=None,loadPath=None):
        self.nodePath = nodePath
        self.loadPath = loadPath
        self.allLoadDict = {}
        self.allNodeDict = {}
    

    def __getAllNode(self):
        assert self.allNodeDict is not None , 'the load path is None, plase input correct path'
        with open(self.allNodeDict,'r') as ftp:
            for line in ftp:
                line = line.replace('(','').replace(')','')
                NodeInformation = line.split(',')
                self.allNodeDict[NodeInformation[0]] = Node(NodeInformation[0],
                                                        NodeInformation[1],NodeInformation[2],
                                                        NodeInformation[3],NodeInformation[4])
        return 
    
    def __getAllLoad(self):
        assert self.allLoadDict is not None 
        with open(self.allLoadDict,'r') as ftp:
            for line in ftp:
               line = line.replace('(','').replace(')','') 
               RoadInformation = line.split(',')
               self.allLoadDict[RoadInformation[0]] = Load(RoadInformation[0],
                                                        RoadInformation[1],RoadInformation[2],
                                                        RoadInformation[3],RoadInformation[4],
                                                        RoadInformation[5],RoadInformation[6])
        return 
    
    def __UnicomNode(self,Node,LoadID,NodeIdList,roadList):
        if self.allLoadDict[LoadID].startNodeID == Node.Id:
            NodeIdList.append(self.allLoadDict[LoadID].endNodeID)
            roadList.append(LoadID)
        elif self.allLoadDict[LoadID].endNodeID == Node.Id and self.allLoadDict[LoadID].Flag:
            NodeIdList.append(self.allLoadDict[LoadID].startNodeID)
            roadList.append(LoadID)
    
    def __getUnicomNode(self,Node):
        NodeIdList = []
        roadList = []
        NodeIdList = self.__UnicomNode(Node,Node.UpLoadID,NodeIdList,roadList)
        NodeIdList = self.__UnicomNode(Node,Node.RightLoadID,NodeIdList,roadList)
        NodeIdList = self.__UnicomNode(Node,Node.DownLoadID,NodeIdList,roadList)
        NodeIdList = self.__UnicomNode(Node,Node.LeftLoadID,NodeIdList,roadList)
        
        return NodeIdList,roadList
            
        
    def __getAdjacencyMatrix(self):
        AdjMax = {}
        
        for key in self.allNodeDict:
            AdjMax[key] = {}
            for key2 in self.allNodeDict:
                AdjMax[key][key2] = []
            
            Node = self.allNodeDict[key]
            NodeIdList,roadIdList = self.__getUnicomNode(Node)
            for NodeID,roadId in zip(NodeIdList,roadIdList):
                AdjMax[key][NodeID].append(roadId)
                      
#更新每辆车的当前路段，和当前路段需要的时间
class disposeCarQueue():
    def __init__(self,carqueue=None,allLoadDict=None,allNodeDict=None):
        self.carqueue = carqueue
        self.fristUpdataRoadCat = None
        self.allLoadDict = {}
        self.allNodeDict = {}
        self.index = None

    def copy(self):
        newClass = disposeCarQueue()
        newClass.allLoadDict  = self.allLoadDict.copy()
        newClass.allNodeDict = self.allNodeDict.copy()
        newClass.carqueue = self.carqueue.copy()
        newClass.fristUpdataRoadCat = self.fristUpdataRoadCat
        newClass.index = self.index
        return newClass

    
#更新每辆车的当前路段，和当前路段需要的时间
class disposeCarQueue():
    def __init__(self,carqueue=None,allLoadDict=None,allNodeDict=None):
        self.carqueue = carqueue
        self.fristUpdataRoadCat = None
        self.allLoadDict = {}
        self.allNodeDict = {}
        self.index = None

    def copy(self):
        newClass = disposeCarQueue()
        newClass.allLoadDict  = self.allLoadDict.copy()
        newClass.allNodeDict = self.allNodeDict.copy()
        newClass.carqueue = self.carqueue.copy()
        newClass.fristUpdataRoadCat = self.fristUpdataRoadCat
        newClass.index = self.index
        return newClass

    def __fristUpdataRoadCat(self):
        MinNowRoadcostTime = const.Maxvalue
        index = -1
        for i in  range(0,len(self.carqueue)):
            if MinNowRoadcostTime >= self.carqueue[i].nowadayRoadNeedTime:
                MinNowRoadcostTime = self.carqueue[i].nowadayRoadNeedTime
                index = i
        self.index = index 
        self.fristUpdataRoadCat = self.carqueue[index]

    def addCat(self,cat):
        self.carqueue.append(cat)
        return

    def __removeCat(self,fisrtCat):
        if fisrtCat.nextRoadID is None:
            del self.carqueue[self.index]
            return True
        return False

    def updataQueue(self):
        for i in  range(0,len(self.carqueue)):
            if self.index == i:
               self.__updataFisrtCat(self.carqueue[i])
            else:
                self.__updataOrdinaryCar(self.carqueue[i])
                
    def __updataOrdinaryCar(self,ordinaryCat):
        ordinaryCat.nowadayRoadNeedTime -= self.carqueue[self.index].nowadayRoadNeedTime

    def __updataFisrtCat(self,fisrtCat):
        if self.__removeCat(fisrtCat):
            fisrtCat.index += 1
            fisrtCat.nowadayRoadID = fisrtCat.bestWaylist[fisrtCat.index]
            self.__updataspeed(fisrtCat)

            if len(fisrtCat.bestWaylist) > fisrtCat.index + 1:
                fisrtCat.nextRoadID = fisrtCat.bestWaylist[fisrtCat.index + 1]
            else:
                fisrtCat.nextRoadID = None

    def __updataspeed(self,Cat):
        MaxTime = self.allLoadDict[Cat.nowadayRoadID].length/...
        min([self.allLoadDict[Cat.nowadayRoadID].maxspeep,Cat.maxspeed])

        for i in  range(0,len(self.carqueue)):
            if i !=  self.index:
                if Cat.nowadayRoadID == self.carqueue[i].nowadayRoadID:
                    if MaxTime < self.carqueue[i].nowadayRoadNeedTime:
                        MaxTime = self.carqueue[i].nowadayRoadNeedTime

        Cat.nowspeed = self.allLoadDict[Cat.nowadayRoadID].length/MaxTime
        Cat.nowadayRoadNeedTime = MaxTime

    def __replaceLoadCatList():
