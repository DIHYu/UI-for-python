
from pyeasyDesign import pyeasyUI  as pyUI
from PyQt5.QtWidgets import QApplication, QWidget
import sys


class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()        
        self.resize(800,600)
        
#        self.base = Test(parent = self, size = [300,300], pic = 'test.jpg')
        
        #初始化
        self.test = pyUI.easyButton(parent = self, size = [300,300], pic = 'test.jpg')
	#按鈕變換
        self.test.setButtonAction(mode = 'conversion', tPixmap = 'test3.jpg')
        self.temp = 0
	#滑鼠單點發光
        self.test.clicked.connect(lambda : self.buttonCheck())
	#滑鼠雙擊移動
        self.test.doubleClicked.connect(lambda : self.test.moveAction(check = True, time = 10, position = [500, 300], mode = 'normal'))
        
# =============================================================================
#         self.test2 = pyUI.easyLabel(parent = self, size = [600,600], pic = 'test2.jpg')
#         self.test2.setPageAttributes(page = 3, position = [0, 0],rollRange = 200)
# =============================================================================
        
        self.show()

    def buttonCheck(self):
    
        if self.temp ==0:
            self.test.changeAction(check = True, time = 300, pic = ['test3.jpg'])
            self.temp = 1
        else:
            self.temp = 0
            self.test.changeAction(check = False)


class Test(pyUI.easyLabel):
    
    def __init__(self, parent, size = [0,0], position = [0, 0], pic = ''):
        
        super().__init__(parent, size, position, pic)
        
        
        


app = QApplication(sys.argv)
MainWindow = MainWindow()
sys.exit(app.exec_())




