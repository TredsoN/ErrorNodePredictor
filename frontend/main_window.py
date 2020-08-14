'''
***********************
程序主界面
***********************
'''

import sys
import csv
import numpy as np

from time import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from frontend.draw_topology import NodeTopology
from backend.interface import get_node, get_information

class PredictorUI(QMainWindow):
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
    _wrongNode = -1
    _data = []
    _filenames = set()
    _curdata = None
    
    def __init__(self):
        super().__init__()
        loadUi("frontend/resources/MainWindow.ui",self)

        self.setWindowTitle('Predictor')
        self.setup_event()
        self.setup_topoloy_view()
    
    ## 初始化点击事件
    def setup_event(self):
        self.loading.hide()
        filecss = '''
            QPushButton{border-image: url(frontend/resources/file.png)}
            QPushButton:hover{border-image: url(frontend/resources/file2.png)}
        '''
        savecss = '''
            QPushButton{border-image: url(frontend/resources/down.png)}
            QPushButton:hover{border-image: url(frontend/resources/down2.png)}
        '''
        clearcss = '''
            QPushButton{border-image: url(frontend/resources/clear.png)}
            QPushButton:hover{border-image: url(frontend/resources/clear2.png)}
        '''
        self.file.setStyleSheet(filecss)
        self.save.setStyleSheet(savecss)
        self.clear.setStyleSheet(clearcss)
        self.sys1.clicked.connect(lambda:self.show_systopo(1))
        self.sys2.clicked.connect(lambda:self.show_systopo(2))
        self.sys3.clicked.connect(lambda:self.show_systopo(3))
        self.sys4.clicked.connect(lambda:self.show_systopo(4))
        self.sys5.clicked.connect(lambda:self.show_systopo(5))
        self.sys6.clicked.connect(lambda:self.show_systopo(6))
        self.sys7.clicked.connect(lambda:self.show_systopo(7))
        self.sys8.clicked.connect(lambda:self.show_systopo(8))
        self.sys9.clicked.connect(lambda:self.show_systopo(9))
        self.sys10.clicked.connect(lambda:self.show_systopo(10))
        self.file.clicked.connect(self.choose_files)
        self.save.clicked.connect(self.save_result)
        self.clear.clicked.connect(self.clear_all)

    ## 初始化拓扑视图
    def setup_topoloy_view(self):
        wrongSys = 0
        if self._curdata == None:
            self._wrongNode = -1
        else:
            self._wrongNode = self._curdata[2]
            for i in range(10):
                if self._wrongNode in self._sysNodes[i]:
                    wrongSys = i+1
                    break
        cssstrori = '''
            QPushButton{border-bottom-width: 0px}
            QPushButton{background-color: rgb(0, 170, 255)}
	        QPushButton{border-radius: 35px}
	        QPushButton{font: 12pt "Microsoft YaHei"}
            QPushButton:hover{background-color:rgb(0, 147, 220)}
        '''
        cssstr = '''
            QPushButton{border-bottom-width: 0px}
            QPushButton{background-color:'#E31015'}
            QPushButton{border-radius:35px}
            QPushButton{font: 12pt 'Microsoft YaHei'}
            QPushButton:hover{background-color:'#c70e14'}
        '''
        self.sys1.setStyleSheet(cssstrori)
        self.sys2.setStyleSheet(cssstrori)
        self.sys3.setStyleSheet(cssstrori)
        self.sys4.setStyleSheet(cssstrori)
        self.sys5.setStyleSheet(cssstrori)
        self.sys6.setStyleSheet(cssstrori)
        self.sys7.setStyleSheet(cssstrori)
        self.sys8.setStyleSheet(cssstrori)
        self.sys9.setStyleSheet(cssstrori)
        self.sys10.setStyleSheet(cssstrori)
        if wrongSys == 1:
            self.sys1.setStyleSheet(cssstr)
        elif wrongSys == 2:
            self.sys2.setStyleSheet(cssstr)
        elif wrongSys == 3:
            self.sys3.setStyleSheet(cssstr)
        elif wrongSys == 4:
            self.sys4.setStyleSheet(cssstr)
        elif wrongSys == 5:
            self.sys5.setStyleSheet(cssstr)
        elif wrongSys == 6:
            self.sys6.setStyleSheet(cssstr)
        elif wrongSys == 7:
            self.sys7.setStyleSheet(cssstr)
        elif wrongSys == 8:
            self.sys8.setStyleSheet(cssstr)
        elif wrongSys == 9:
            self.sys9.setStyleSheet(cssstr)
        elif wrongSys == 10:
            self.sys10.setStyleSheet(cssstr)
        
        nodeTopo = NodeTopology(self.topologyview, wrongSys if wrongSys!=0 else 1, wrongId=self._wrongNode)
        nodeTopo.move(0,0)

    ## 左侧列表增加新的结果
    def append_left(self, data):
        item = QListWidgetItem()
        item.setSizeHint(QSize(300, 120))
        self.resultlist.addItem(item)
        self.resultlist.setItemWidget(item, self.get_list_item(data))

    # 生成列表项
    def get_list_item(self, data):
        btn = QPushButton()
        btn.resize(298,120)
        btn.setStyleSheet('''
            QWidget{
                border-right-width: 0px; 
                border-bottom: 1px solid #dedede; 
                background-color: rgb(50, 50, 50);
            }
            QWidget:hover{
                border-bottom: 3px solid rgb(255, 255, 255);
            }
        ''')
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda: self.change_file(data))

        item = QWidget(btn)
        item.resize(298, 120)
 
        label1 = QLabel(item)
        label2 = QLabel(item)
        label3 = QLabel(item)
        label1.setText(data[0])
        label2.setText("has root: %s" % ('yes' if data[1] == 'Y' else 'no'))
        label3.setText("root node: %d" % (data[2]) if data[2] !='' else '')
        label1.setWordWrap(True)
        label1.setGeometry(5, 10, 288, 60)
        label2.setGeometry(5, 80, 144, 30)
        label3.setGeometry(149, 80, 144, 30)
        label1.setStyleSheet('QLabel{border-bottom-width: 0px; font: 10pt "Microsoft YaHei"; color: #ffffff}')
        if data[1] == 'Y':
            btn.setToolTip("Trigger: " + data[3])
            label2.setStyleSheet('QLabel{border-bottom-width: 0px; font: 10pt "Microsoft YaHei"; color: #E31015}')
            label3.setStyleSheet('QLabel{border-bottom-width: 0px; font: 10pt "Microsoft YaHei"; color: #E31015}')
        else:
            label2.setStyleSheet('QLabel{border-bottom-width: 0px; font: 10pt "Microsoft YaHei"; color: #64F000}')
            label3.setStyleSheet('QLabel{border-bottom-width: 0px; font: 10pt "Microsoft YaHei"; color: #64F000}')
        
        return btn

    ## 修改文件
    def change_file(self, data):
        self._curdata = data
        self.setWindowTitle('Result-' + self._curdata[0])
        self.setup_topoloy_view()

    ## 显示提示
    def show_message(self, text):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Message")
        message.setText(text)
        message.exec_()

    #### 点击事件
    ## 切换系统拓扑视图
    def show_systopo(self, sysId):
        nodeTopo = NodeTopology(self.topologyview, sysId, wrongId=self._wrongNode)
        nodeTopo.move(0, 0)

    ## 保存预测结果
    def save_result(self):
        if len(self._data) == 0:
            self.show_message("No results can be saved.")
            return

        self.txtloading.setText('Saving...')
        self.loading.show()
        save_path, ok2 = QFileDialog.getSaveFileName(self, "Save results", "../", "CSV Files (*.csv)")
        if save_path == '':
            self.show_message("Saving cancelled.")
            self.loading.hide()
            return
        with open(save_path, 'w', newline='', encoding='UTF-8') as file:
            data = self._data
            data.insert(0, ['file path', 'has root', 'root node', 'trigger'])
            data = np.array(data)
            writer = csv.writer(file)
            writer.writerows(data)
        self.show_message("Saved successfully.")
        self.loading.hide()
    
    ## 选择文件
    def choose_files(self):
        self.txtloading.setText('Analyzing...')
        self.loading.show()
        file_names, file_types = QFileDialog.getOpenFileNames(self,  
                                "Choose files.",
                                "../",
                                "CSV Files (*.csv)")

        file_names = set(file_names) - self._filenames
        self._filenames.update(file_names)

        start_time = time()
        if len(file_names) == 0:
            self.show_message("No new files selected.")
            self.loading.hide()
            return

        for file_name in file_names:
            try:
                result = (file_name, get_node(file_name))
                row = None
                if result[1] == -1:
                    row = (result[0], 'N', '', '')
                else:
                    reason = get_information(file_name, result[1])
                    row = (result[0], 'Y', result[1], reason)
                self._data.append(row)
                self.append_left(row)
            except:
                self.show_message("Unrecognized file content:\n" + file_name)
        end_time = time()
        print((end_time - start_time))


        self.instruction.hide()
        self.loading.hide()
    
    ## 清空结果
    def clear_all(self):
        if len(self._data) == 0:
            self.show_message("No results can be deleted.")
            return
        
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Message")
        message.setText("Confirm to delete all results?")
        message.addButton("yes", QMessageBox.AcceptRole)
        msg_no = message.addButton("no", QMessageBox.NoRole)
        message.setDefaultButton(msg_no)
        reply = message.exec_()

        if reply == 1:
	        return
        else:
            while self.resultlist.count() != 0:
                self.resultlist.takeItem(0)
            self._wrongNode = -1
            self._data = []
            self._filenames = set()
            self._curdata = None
            self.setWindowTitle('Predictor')
            self.setup_topoloy_view()
            self.instruction.show()