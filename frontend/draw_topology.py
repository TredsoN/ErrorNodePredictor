'''
***********************
绘制拓扑图
***********************
'''

import math
import matplotlib.pyplot as plt
import networkx as nx

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class NodeTopology(FigureCanvas):
    _sysNodes = (
        (50,0,58,4,83,33,17,31,15,73,93),
        (70,30,45,37,55,21,18,7,99,8,91),
        (57,20,28,3,97,39,86,94),
        (72,34,81,36,62,77,69,13,9,19,27,5),
        (14,26,65,2,76,38,82,60,6,74,85),
        (56,67,25,48,59,32,35,46,1,98),
        (63,53,61,89,54,24,23,51),
        (84,10,49,95,88,43,41,71,79,87),
        (68,16,92,78,47,75,22,80,66,12,44),
        (29,64,96,42,90,11,52,40)
    )
    _nodeEdges = {
        50:(4,83,33,17),0:(4,83,33,17),58:(4,83,33,17),
        4:(31,15,73,93),83:(31,15,73,93),33:(31,15,73,93),17:(31,15,73,93),
        70:(37,55,21),30:(37,55,21),45:(37,55,21),
        37:(18,7,99,8,91),55:(18,7,99,8,91),21:(18,7,99,8,91),
        57:(28,3,97),20:(28,3,97),
        28:(39,86,94),3:(39,86,94),97:(39,86,94),
        72:(62,77),34:(62,77),81:(62,77),36:(62,77),
        62:(69,13,9,19,27,5),77:(69,13,9,19,27,5),
        14:(65,2,76,38),26:(65,2,76,38),
        65:(82,60,6,74,85),2:(82,60,6,74,85),76:(82,60,6,74,85),38:(82,60,6,74,85),
        56:(25,48,59,32),67:(25,48,59,32),
        25:(35,46,1,98),48:(35,46,1,98),59:(35,46,1,98),32:(35,46,1,98),
        63:(61,89),53:(61,89),
        61:(54,24,23,51),89:(54,24,23,51),
        84:(88,43,41),10:(88,43,41),49:(88,43,41),95:(88,43,41),
        88:(71,79,87),43:(71,79,87),41:(71,79,87),
        68:(47,75),16:(47,75),92:(47,75),78:(47,75),
        47:(22,80,66,12,44),75:(22,80,66,12,44),
        29:(42,90,11),64:(42,90,11),96:(42,90,11),
        42:(52,40),90:(52,40),11:(52,40),
        31:(63,53,68,16,92,78),15:(63,53,68,16,92,78),73:(63,53,68,16,92,78),93:(63,53,68,16,92,78),
        18:(84,10,49,95),7:(84,10,49,95),99:(84,10,49,95),8:(84,10,49,95),91:(84,10,49,95),
        39:(56,67,84,10,49,95),86:(56,67,84,10,49,95),94:(56,67,84,10,49,95),
        69:(50,0,58,14,26),13:(50,0,58,14,26),9:(50,0,58,14,26),19:(50,0,58,14,26),27:(50,0,58,14,26),5:(50,0,58,14,26),
        82:(56,67,63,53),60:(56,67,63,53),6:(56,67,63,53),74:(56,67,63,53),85:(56,67,63,53),
        35:(72,34,81,36,29,64,96),46:(72,34,81,36,29,64,96),1:(72,34,81,36,29,64,96),98:(72,34,81,36,29,64,96),
        54:(57,20,29,64,96),24:(57,20,29,64,96),23:(57,20,29,64,96),51:(57,20,29,64,96),
        71:(72,34,81,36),79:(72,34,81,36),87:(72,34,81,36),
        22:(70,30,45),80:(70,30,45),66:(70,30,45),12:(70,30,45),44:(70,30,45),
        52:(72,34,81,36,70,30,45),40:(72,34,81,36,70,30,45),
    }

    def __init__(self, parent, sysId=1, wrongId=-1):
        self._sysId = sysId
        self._wrongId = wrongId

        for child in parent.children():
            del child

        fig = Figure(figsize=(10, 7), dpi=100, facecolor='black')
        self.axes = fig.add_subplot(111)
        self.axes.set_title(label='System ' + str(sysId), fontdict={'fontsize':20,'color':'white'})
        self.axes.set_axis_off()
        self.axes.set_facecolor('black')

        FigureCanvas.__init__(self, fig)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.plot()

    def plot(self):
        ## 计算拓扑图中的边
        finEdges = []
        for node in self._sysNodes[self._sysId-1]:
            for end in self._nodeEdges[node]:
                # 当前系统内部的边
                if end in self._sysNodes[self._sysId-1]:
                    finEdges.append((node,end))
                # 指向另一个系统的边
                else:
                    for i in range(0,10):
                        if end in self._sysNodes[i]:
                            finEdges.append((node,i+101))
                            break
        ## 创建拓扑图
        G = nx.DiGraph()
        G.add_edges_from(list(set(finEdges)))
        ## 统计图中系统节点数目
        syscnt = 0
        for node in G.nodes:
            if node > 100:
                syscnt += 1
        ##分离图中不同的节点，同时计算每个节点在图中的位置和标签
        sysNodes = []
        wrongNodes = []
        normalNodes = []
        labels = {}
        positions = {}
        nodecnt = len(G.nodes)-syscnt if self._wrongId not in self._sysNodes[self._sysId-1] else len(G.nodes)-syscnt-1
        nodeindex = 0
        sysindex = 0
        syspos = [[4,-1],[4,1]]
        for node in G.nodes:
            angle = 2*nodeindex*math.pi/nodecnt
            if node > 100:
                sysNodes.append(node)
                labels[node] = node-100
                positions[node] = syspos[sysindex]
                sysindex += 1
            elif node == self._wrongId:
                wrongNodes.append(node)
                labels[node] = node
                positions[node] = [0,0]
            else:
                normalNodes.append(node)
                labels[node] = node
                positions[node] = [2*math.cos(angle),2*math.sin(angle)]
                nodeindex += 1
        ## 绘制拓扑图
        nx.draw_networkx_nodes(G, pos=positions, ax=self.axes, nodelist=sysNodes, node_color='#00aaff', node_size=700, edgecolors='k')
        nx.draw_networkx_nodes(G, pos=positions, ax=self.axes, nodelist=wrongNodes, node_color='#E31015', node_size=700, edgecolors='k')
        nx.draw_networkx_nodes(G, pos=positions, ax=self.axes, nodelist=normalNodes, node_color='#64F000', node_size=700, edgecolors='k')
        nx.draw_networkx_edges(G, pos=positions, ax=self.axes, edge_color='white',  arrowstyle='->', arrowsize=20, min_source_margin=13, min_target_margin=13)
        nx.draw_networkx_labels(G, pos=positions, labels=labels, ax=self.axes, font_family='Microsoft YaHei', font_size=14)
        self.show()