from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QPoint
import numpy as np

class easyMode(QLabel):
    
    def __init__(self, parent, objectSelf, pixmap):

        super().__init__(parent)
        
        self.initCheck = {'picChangeMode' : False, 'picMoveMode' : False}
        
        self.objectSelf = objectSelf
        
        self.pixmap = pixmap    
        
    
    def modeCheck(self, mode = '', check = True, size = [0,0], position = [0, 0],  
                  tPixmap = QPixmap, cPixmap = [], time = 0):
    
        """
        This is a passing data module function.
        
        Parameters:
            
            mode - Confirm where the module is delivered.
            check - Confirm module usage status.
            size - Pass size to modules. 
            position - Pass position to modules.
            cPixmap - Pass a pixmap list to modules.
            tPixmap - Pass a pixmap to modules.
            time - Pass time to modules
        
        Returns:
            
            This function does no return.
            
        """
        
        if mode == 'scale' :
            self.scaleMode(check = check, size = size)
            
        elif mode == 'conversion':
            self.conversionMode(check = check, tPixmap = tPixmap)
                
        elif mode == 'picChange':
            self.cPixmap = [self.pixmap]
            for i in cPixmap:
                self.cPixmap.append(i)
            self.picChangeMode(check = check, time = time)
            
                
# =============================================================================
# 縮放模式    
# =============================================================================
    def scaleMode(self, check = '', size = [0,0], cPixmap = QPixmap):
        
        """
        This is a function for scale picture.
        
        Parameters:
            
            check - Confirm module usage status.
            size - Pass size to modules. 
            cPixmap - The picture for this scale action.
        
        Returns:
            
            This function does no return.
            
        """

        if check:
            self.objectSelf.resize(size[0]+30, size[1]+30)
            self.objectSelf.setPixmap(self.pixmap.scaled(size[0]+30, size[1]+30))
        
        else:
            self.objectSelf.resize(size[0]-30, size[1]-30)
            self.objectSelf.setPixmap(self.pixmap.scaled(size[0]-30, size[1]-30))

# =============================================================================
# 轉換模式
# =============================================================================

    def conversionMode(self, check = '', tPixmap = QPixmap):
        
        """
        This is a function for conversion picture.
        
        Parameters:
            
            check - Confirm module usage status.
            tPixmap - The picture for this conversion action.
        
        Returns:
            
            This function does no return.
            
        """
        if check:
            self.objectSelf.setPixmap(tPixmap)
        
        else:
            self.objectSelf.setPixmap(self.pixmap)


# =============================================================================
# 獨
# 立
# 模
# 組            
# =============================================================================
            
# =============================================================================
# 圖片切換模式    
# =============================================================================
    def picChangeMode(self,check = True, time = 0):
        
        """
        This is a function for change picture.
        
        Parameters:
            
            check - Confirm module usage status.
            time - Pass time to modules
        
        Returns:
            
            This function does no return.
            
        """
        
        if not self.initCheck['picChangeMode'] :     
            self.picChangeTimer = QTimer(self)
            self.picChangeTimer.timeout.connect(self.picChangeModeTimer)
            self.initCheck['picChangeMode'] = True
            print('picChangeMode __init__')            
        
        if check:
            self.cPixmapTemp = 1
            self.objectSelf.setPixmap(self.pixmap.scaled(self.objectSelf.size()))

            self.picChangeTimer.start(time)
            
        else:
            print('changeStop')
            self.picChangeTimer.stop()
            self.objectSelf.setPixmap(self.pixmap.scaled(self.objectSelf.size()))
# =============================================================================
# 圖片切換模式(計時器)             
# =============================================================================
    def picChangeModeTimer(self):

        self.objectSelf.setPixmap(self.cPixmap[self.cPixmapTemp].scaled(self.objectSelf.size()))
        if self.cPixmapTemp == len(self.cPixmap)-1:
            self.cPixmapTemp = 0
        else:
            self.cPixmapTemp += 1

# =============================================================================
# 圖片移動模式
# =============================================================================
    
    def picMoveMode(self, check = True, time = 0, position = [0,0], mode = 'normal'):
        
        """
        This is a function for move picture.
        
        Parameters:
            
            mode - Confirm where the module is delivered.
            check - Confirm module usage status.
            position - Pass position to modules.
            time - Pass time to timer.
        
        Returns:
            
            This function does no return.
            
        """
        
        self.mode = mode
        
        if not self.initCheck['picMoveMode']:
            self.picMoveTimer = QTimer(self)
            self.picMoveTimer.timeout.connect(self.picMoveModeTimer)
            self.initCheck['picMoveMode'] = True
            
        if check:
            self.movePosition = position
            self.picMoveTimer.start(time)
            
            
            grid = int((abs(position[0] - self.objectSelf.pos().x()) + 
                    abs(position[1] - self.objectSelf.pos().y()))/2)
            
            self.movegridX = np.linspace(self.objectSelf.pos().x(), position[0], grid, endpoint=True)
            
            self.movegridY = np.linspace(self.objectSelf.pos().y(), position[1], grid, endpoint=True)
            self.moveTimeTemp = 1 
            
        else:
            self.picMoveTimer.stop()
            
# =============================================================================
# 圖片移動模式(計時器)    
# =============================================================================
    def picMoveModeTimer(self):
        
        if self.mode == 'normal':
            if self.moveTimeTemp < len(self.movegridX):
                self.objectSelf.move(self.movegridX[self.moveTimeTemp], self.movegridY[self.moveTimeTemp])
                self.moveTimeTemp += 1
            else:
                print('stop')
                self.picMoveTimer.stop()
            
            
            
            
        
        
            
        
        
        
        
        
        