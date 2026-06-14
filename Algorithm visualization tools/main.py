import sys
from PyQt5.QtWidgets import QApplication
from gui import AlgorithmGUI    # 從gui.py匯入主視窗類別

# Python程式進入點
if __name__ == "__main__":
    app = QApplication(sys.argv)    #建立 QApplication 物件 (Qt 應用程式物件，所有GUI都需要它)
    window = AlgorithmGUI()         #建立主視窗
    window.show()                   #顯示視窗
    sys.exit(app.exec_())           #進入 Qt 事件迴圈 (保持GUI持續運作)
