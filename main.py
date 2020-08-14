'''
***********************
程序入口
***********************
'''

import sys
from PyQt5.QtWidgets import *
from frontend.main_window import PredictorUI

if __name__=='__main__':
    app = QApplication(sys.argv)
    md = PredictorUI()
    md.show()
    sys.exit(app.exec_())