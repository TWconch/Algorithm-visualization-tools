import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QFrame, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 預設字體，等 QApplication 建立後再更新
default_font_family = "Arial"
plt.rcParams["font.sans-serif"] = [default_font_family]
plt.rcParams["axes.unicode_minus"] = False

# 匯入演算法實作，演算法本身放在 algorithms.py
from algorithms import bubble_sort, insertion_sort

class AlgorithmGUI(QWidget):
    def __init__(self):
        super().__init__()

        # 設定視窗標題和初始大小
        self.setWindowTitle("排序演算法視覺化")
        self.setGeometry(400, 200, 1100, 720)

        # 透過 QApplication 建立後再取得系統字體
        font_db = QFontDatabase()
        if "Microsoft JhengHei" in font_db.families():
            default_font_family = "Microsoft JhengHei"
        elif "Microsoft YaHei" in font_db.families():
            default_font_family = "Microsoft YaHei"
        elif "SimHei" in font_db.families():
            default_font_family = "SimHei"
        elif "Noto Sans CJK TC" in font_db.families():
            default_font_family = "Noto Sans CJK TC"
        else:
            default_font_family = font_db.families()[0] if font_db.families() else "Arial"

        plt.rcParams["font.sans-serif"] = [default_font_family]
        plt.rcParams["axes.unicode_minus"] = False

        # 全域樣式：背景色、標籤、按鈕樣式
        self.setStyleSheet(
            "QWidget { background-color: #f5f7fb; }"
            "QLabel { color: #333; }"
            "QPushButton { background-color: #4a90e2; color: white; border-radius: 12px; padding: 20px; }"
            "QPushButton:hover { background-color: #3b77c1; }"
            "QPushButton:pressed { background-color: #2f63a0; }"
        )

        # 主區塊：左右分割，左側為控制區，右側為動畫區
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(18)
        self.setLayout(main_layout)

        # 左側控制區框架，白色底色讓控制區更有層次感
        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.StyledPanel)
        left_frame.setStyleSheet("QFrame { background-color: white; border: 1px solid #d9dee6; border-radius: 12px; }")
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(18, 18, 18, 18)
        left_layout.setSpacing(12)
        left_frame.setLayout(left_layout)
        main_layout.addWidget(left_frame, 2)

        # 主標題
        title_label = QLabel("排序演算法教學")
        title_label.setFont(QFont("Microsoft JhengHei", 30, QFont.Bold))
        left_layout.addWidget(title_label)

        # 說明文字
        self.info_label = QLabel("請選擇演算法來開始動畫顯示。")
        self.info_label.setWordWrap(True)
        self.info_label.setFont(QFont("Microsoft JhengHei", 14))
        self.info_label.setStyleSheet("QLabel { color: #555; }")
        left_layout.addWidget(self.info_label)

        # 按鈕排列區域，放兩個排序按鈕
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        left_layout.addLayout(button_layout)

        bubble_btn = QPushButton("Bubble Sort")
        bubble_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        bubble_btn.clicked.connect(lambda: self.run_algorithm("bubble"))
        button_layout.addWidget(bubble_btn)

        insert_btn = QPushButton("Insertion Sort")
        insert_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        insert_btn.clicked.connect(lambda: self.run_algorithm("insertion"))
        button_layout.addWidget(insert_btn)

        # 狀態欄顯示目前操作進度，可在其他地方加入更多狀態資訊
        self.status_label = QLabel("目前狀態: 等待選擇演算法")
        self.status_label.setWordWrap(True)
        self.status_label.setFont(QFont("Microsoft JhengHei", 10))
        self.status_label.setStyleSheet("QLabel { color: #666; }")
        left_layout.addWidget(self.status_label)

        left_layout.addStretch(1)

        # 右側動畫區：matplotlib 畫布放在 Qt 中顯示
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor("#f5f7fb")
        self.ax.set_facecolor("#fafbff")
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas, 5)

        # 儲存演算法步驟與動畫物件
        self.steps = []
        self.ani = None

    def run_algorithm(self, algo):
        # 測試資料，可改成隨機資料或使用者輸入
        data = [5, 4, 3, 7, 10, 1, 6]
        if algo == "bubble":
            self.steps = bubble_sort(data)
            self.info_label.setText("Bubble Sort: 重複比較相鄰元素，較大的值逐步往後移動。\n時間複雜度 O(n^2)")
        elif algo == "insertion":
            self.steps = insertion_sort(data)
            self.info_label.setText("Insertion Sort: 從未排序區取一個元素插入到已排序區。\n時間複雜度 O(n^2)")

        self.status_label.setText("目前狀態: 正在播放動畫中...")
        self.start_animation()

    def start_animation(self):
        # 每次重新播放時先清除原本軸
        self.ax.clear()
        self.ax.set_facecolor("#fafbff")

        # 第一個步驟的資料用來建立長條圖，後續透過 update 更新高度與顏色
        bar_rects = self.ax.bar(range(len(self.steps[0][0])), self.steps[0][0], align="edge", color="#57a9ff")
        self.ax.set_ylim(0, max(max(s[0]) for s in self.steps) * 1.2)
        self.ax.set_title("排序過程")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color("#d9dee6")
        self.ax.spines["bottom"].set_color("#d9dee6")

        def update(frame):
            arr, (i, j), swapped = self.steps[frame]

            # 重設所有長條為預設色，然後再高亮目前比較/交換元素
            for rect, val in zip(bar_rects, arr):
                rect.set_height(val)
                rect.set_color("#2e2be1")

            if 0 <= i < len(bar_rects):
                bar_rects[i].set_color("#e23737" if swapped else "#f6b93b")
            if 0 <= j < len(bar_rects):
                bar_rects[j].set_color("#e23737" if swapped else "#f6b93b")

            self.status_label.setText(f"目前狀態: 第 {frame + 1} 步 / 共 {len(self.steps)} 步")

        self.ani = animation.FuncAnimation(self.fig, update, frames=len(self.steps), interval=500, repeat=False)
        self.canvas.draw()
