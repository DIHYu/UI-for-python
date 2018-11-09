from pyeasyDesign import pyeasyMode

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QTimer



class easyObject(QLabel):
    
    clicked = pyqtSignal()
    doubleClicked = pyqtSignal()

    def __init__(self, parent, size = [0,0], position = [0, 0], pic = ''):
        
        super().__init__(parent)
# =============================================================================
# 初始化
# =============================================================================
        self.parent = self

        self.resize(size[0], size[1])
        self.move(position[0], position[1])
        
        self.replacePixmap = QPixmap
        
        self.pageAttributes = False
        self.pages = []
        self.pageMode = 'RL'
        self.pagePosition = [0, 0]
        self.rollRange = 0
        
        self.actionCheck  = False
        self.actionMode   = 'scale'
        
        self.pixmap = QPixmap(pic).scaled(self.width(), self.height())
        self.setPixmap(self.pixmap)
        self.tPixmap = QPixmap
        self.easyMode = pyeasyMode.easyMode(parent, objectSelf = self, pixmap = self.pixmap)
        
        self.pressed = False
        self.enter   = False
        
        self.mouseShotCount = 0
        

# =============================================================================
# 圖片交換
# =============================================================================
    def changeAction(self,check = True, time = 0, pic = []): 
        cPixmap = []
        for i in pic:
            cPixmap.append(QPixmap(i))
        self.easyMode.modeCheck(mode = 'picChange', check = check, time = time, cPixmap = cPixmap)
        
        
    def changePicture(self, pic = ''):
        self.pixmap = QPixmap(pic).scaled(self.size())
        
        self.setPixmap(self.pixmap)
        self.easyMode.pixmap = self.pixmap
        
# =============================================================================
# 圖片移動
# =============================================================================
    def moveAction(self, check = True, time = 0 , position = [0,0], mode = 'normal'):
        
        self.easyMode.picMoveMode(check = check, time = time, position = position, mode = mode)
        
        

# =============================================================================
# 滑鼠事件(進入、離開)
# =============================================================================
    def enterEvent(self, e):

        if self.actionCheck == True: 
            self.easyMode.modeCheck(mode = self.actionMode, check = True, size = [self.width(), 
                                                            self.height()], tPixmap = self.tPixmap)
        self.enter = True    
        
    def leaveEvent(self, e): 
        if self.actionCheck == True:          
            self.easyMode.modeCheck(mode = self.actionMode, check = False, size = [self.width(),
                                                                    self.height()], tPixmap = self.tPixmap)
        self.enter = False

# =============================================================================
# 滑鼠事件(點擊、放開)
# =============================================================================
    def mousePressEvent(self, e): 
        self.pressed = True
        self.pressedPointX = e.x()
        self.pressedPointY = e.y()
        
        
    def mouseReleaseEvent(self, e):

        if self.pressed == True and self.enter == True:
            if self.mouseShotCount == 0:
                self.mouseShotCount += 1
                QTimer.singleShot(200, self.mouseShot)
            else:
                self.mouseShotCount += 1
        self.pressed = False
        
        if self.parent.pageAttributes:
            
            if self.parent.pageMode == 'RL':
                if len(self.parent.pages)!= 1:
                    temp = [(abs(self.parent.pages[i] - abs(self.parent.x()))) for i in range(len(self.parent.pages))]
                    self.parent.move((self.parent.pages[temp.index(min(temp))]*-1) - self.parent.pagePosition[0], self.parent.y())

                else:
                    if self.parent.x() > 0 + self.parent.pagePosition[0]:
                        self.parent.move(self.parent.pagePosition[0],self.parent.y())
                        
                    elif abs(self.parent.x()-self.parent.pagePosition[0])+self.parent.rollRange > self.parent.width():
                        self.parent.move((self.parent.rollRange-self.parent.width()) + self.parent.pagePosition[0],self.parent.y())
                        
            elif self.parent.pageMode == 'TB':
                
                if len(self.parent.pages)!= 1:
                    temp = [(abs(self.parent.pages[i] - abs(self.parent.y()))) for i in range(len(self.parent.pages)-1)]
                    self.parent.move(self.parent.x(), (self.parent.pages[temp.index(min(temp))]*-1) - self.parent.pagePosition[0])
                else:
                    if self.parent.y() > 0 + self.parent.pagePosition[1]:
                        self.parent.move(self.parent.x(), self.parent.pagePosition[1])
                        
                    elif abs(self.parent.y()-self.parent.pagePosition[1])+self.parent.rollRange > self.parent.height():
                        self.parent.move(self.parent.x(), (self.parent.rollRange-self.parent.height()) + self.parent.pagePosition[1])


    
        
    def mouseMoveEvent(self, e):
        #if  e.x() > self.width() or e.y() > self.height() or e.x() < 0 or e.y() < 0:
        self.enter = False
            
        if self.parent.pageAttributes:
            
            if self.parent.pageMode == 'RL':
                if self.pressedPointX > e.x():
                    if abs(self.parent.x()-self.parent.pagePosition[0])+self.parent.rollRange < self.parent.width()+10:
                        self.parent.move(self.parent.x()-abs(self.pressedPointX-e.x()), self.parent.y())
                        

                elif self.pressedPointX < e.x() and self.parent.x() < 10 + self.parent.pagePosition[0]:
                    self.parent.move(self.parent.x()+abs(self.pressedPointX-e.x()), self.parent.y())
                    
            elif self.parent.pageMode == 'TB':
                
                #print(self.pressedPointY, e.y())
                if self.pressedPointY > e.y():
                    if abs(self.parent.y()-self.parent.pagePosition[1])+self.parent.rollRange < self.parent.height()+10:
                        self.parent.move(self.parent.x(), self.parent.y()-abs(self.pressedPointY-e.y()))
                        
                elif self.pressedPointY < e.y() and self.parent.y() < 10 + self.parent.pagePosition[1]:
                    self.parent.move(self.parent.x(), self.parent.y()+abs(self.pressedPointY-e.y()))
        
    
    def mouseShot(self):
        if self.mouseShotCount == 1:
            self.clicked.emit()
        else:
            self.doubleClicked.emit()
        
        
        self.mouseShotCount = 0
    
    def setReplacePixmap(self, pic = ''):
        
        self.replacePixmap = QPixmap(pic).scaled(self.size())
        
    def replacePixmap(self, pic = QPixmap):
        
        self.setPixmap(pic)
    

class easyLabel(easyObject):
    
        
    def __init__(self, parent, size = [300,300], position = [0, 0], pic = ''):
        
        super().__init__(parent = parent, size = size, position = position, pic = pic)
                        
    def setPageAttributes(self, check = True, page = 1, pageMode = 'RL', rollRange = 0, position = [0, 0]):
        self.pageAttributes = check
        self.rollRange = rollRange
        self.pagePosition = position
        self.parent = self
        self.pages.clear()
        self.pageMode = pageMode
        
        if rollRange == 0:
            if pageMode == 'RL':
                x = self.width()/page
            elif pageMode == 'TB':
                x = self.height()/page
                
            for i in range(page):
                self.pages.append(x*i)
        else:
            for i in range(page):
                self.pages.append(i*rollRange)
        print(self.pages)
            
    def setPageParent(self, parent):
        self.parent = parent
        
        
class easyButton(easyObject):

    def __init__(self, parent, size = [0,0], position = [0, 0], pic = ''):

        super().__init__(parent = parent, size = size, position = position, pic = pic)
    
    def setButtonAction(self, check = True, mode = 'scale', tPixmap = ''):
        
        self.actionCheck = check
        self.actionMode  = mode
        
        if tPixmap != '':
            self.tPixmap = QPixmap(tPixmap).scaled(self.size())
            

            






