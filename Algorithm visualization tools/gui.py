import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 匯入演算法
from algorithms import bubble_sort, insertion_sort

class AlgorithmGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("演算法教學介面")
        self.setGeometry(400, 200, 1080, 720)   # 視窗大小與位置

        # 主版面:水平分割(左邊控制區 + 右邊動畫區)
        layout = QHBoxLayout()
        self.setLayout(layout)


        # -------------------- 左邊控制區 --------------------
        control_layout = QVBoxLayout()
        layout.addLayout(control_layout, 2)

        # 顯示演算法介紹的 Label
        self.info_label = QLabel("請選擇演算法")
        control_layout.addWidget(self.info_label)

        # Bubble Sort 按鈕
        bubble_btn = QPushButton("Bubble Sort")
        bubble_btn.clicked.connect(lambda: self.run_algorithm("bubble"))
        control_layout.addWidget(bubble_btn)

        # Insertion Sort 按鈕
        insert_btn = QPushButton("Insertion Sort")
        insert_btn.clicked.connect(lambda: self.run_algorithm("insertion"))
        control_layout.addWidget(insert_btn)

        # -------------------- 右邊動畫區 --------------------
        self.fig, self.ax = plt.subplots()      # 建立 matplotlib 繪圖區
        self.canvas = FigureCanvas(self.fig)    # 崁入到 PyQt 視窗
        layout.addWidget(self.canvas, 5)        # 右邊區域佔 5 權重

        # 儲存演算法步驟
        self.steps = []
        self.ani = None

    # 當使用者點選某個演算法時，呼叫這個函式
    def run_algorithm(self, algo):
        data = [5, 4, 3, 7, 10, 1, 6]   # 測試用資料
        if algo == "bubble":
            self.steps = bubble_sort(data)
            self.info_label.setText("Bubble Sort: 重複比較相鄰元素，較大的往後移動。\n時間複雜度 O(n^2)")
        elif algo == "insertion":
            self.steps = insertion_sort(data)
            self.info_label.setText("Insertion Sort: 從未排序部分取一個插入到已排序部分。\n時間複雜度 O(n^2)")

        self.start_animation()

    # 播放動畫
    def start_animation(self):
        self.ax.clear()  # 清除舊的圖表

        # 初始化長條圖（第一個步驟的狀態）
        bar_rects = self.ax.bar(range(len(self.steps[0][0])), self.steps[0][0], align="edge")
        self.ax.set_ylim(0, max(max(s[0]) for s in self.steps) * 1.1)  # y 軸上限設為數值最大值的 1.1 倍
        
        # 每一幀動畫更新函式
        def update(frame):
            arr, (i, j), swapped = self.steps[frame]
            for rect, val in zip(bar_rects, arr):
                rect.set_height(val)    # 更新每個長條高度
                rect.set_color("cyan")  # 預設顏色

            # 高亮顯示目前比較/交換的元素
            if 0 <= i < len(bar_rects):
                bar_rects[i].set_color("red" if swapped else "yellow")
            if 0 <= j < len(bar_rects):
                bar_rects[j].set_color("red" if swapped else "yellow")

        # 建立動畫     
        self.ani = animation.FuncAnimation(self.fig, update, frames=len(self.steps), interval=500, repeat=False)
        self.canvas.draw()
