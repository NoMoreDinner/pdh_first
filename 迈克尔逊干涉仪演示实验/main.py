import numpy,math
from Myfun import wavelength_to_map
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication , QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import pyqtSlot
from UiApp import Ui_MainWindow
from numpy import pi, linspace ,meshgrid ,sin ,square, sqrt, power, tan, cos, arctan, max
from scipy.special import jv
from matplotlib import font_manager, pyplot
import sys
import os
# 导入字体管理模块



class MainApp(QMainWindow , Ui_MainWindow):

    def __init__(self):
        self.SongTi = font_manager.FontProperties(fname="C:/WINDOWS/Fonts/STSONG.TTF")
        QMainWindow.__init__(self)
        self.font = {'family': 'Times New Roman',
                     'weight': 'bold',
                     'style': 'normal',
                     'size': 16,
                     }
        self.setupUi(self)
        self.fig()
        self.setpushButton()


    def setpushButton(self):
        self.pushButton_exit.clicked.connect(self.pushButton_exit_Cilicked)
        self.pushButton_recover.clicked.connect(self.pushButton_recover_Cilicked)
        self.pushButton_Save1.clicked.connect(self.pushButton_Save1_Cilicked)
        self.pushButton_return.clicked.connect(self.pushButton_return_Cilicked)
        self.pushButton_Save2.clicked.connect(self.pushButton_Save2_Cilicked)


    def pushButton_exit_Cilicked(self):
        sys.exit(app.exec())


    def pushButton_recover_Cilicked(self):
        self.SpinBox_n.setProperty("value", 1)
        self.SpinBox_d.setProperty("value", 10.00)
        self.SpinBox_x.setProperty("value", 15.00)
        self.SpinBox_f.setProperty("value", 5.0)
        self.SpinBox_N.setProperty("value", 400)
        self.SpinBox_lamda.setProperty("value", 487.2)

    def pushButton_Save1_Cilicked(self):
        name = self.textEdit_name.toPlainText()
        if name == '':
            name = '衍射图像'
        style = self.comboBox_style.currentText()
        str = '图像/' + name + style
        pyplot.imsave(str, self.imgdata, cmap=self.my_cmp)

    def pushButton_return_Cilicked(self):
        self.close()



    def pushButton_Save2_Cilicked(self):
        name = self.textEdit_name.toPlainText()
        if name == '':
            name = '光强分布'
        style = self.comboBox_style.currentText()
        str = '图像/' + name + style
        dpi = int(self.comboBox_N.currentText())
        fig = self.mplwidget_I.canvas.fig
        fig.savefig(str, dpi=dpi)






    def fig(self):  # 计算图像
        lamda = self.SpinBox_lamda.value() * 1e-9
        d = self.SpinBox_d.value() * 1e-3
        x_lim =self.SpinBox_x.value() * 1e-3
        N = int(self.SpinBox_N.value())
        n = self.SpinBox_n.value()
        f = self.SpinBox_f.value() * 1e-2
        x = linspace(-x_lim, x_lim, N)
        [X, Y]= meshgrid(x, x)
        r = sqrt(square(X) + square(Y))
        i = arctan(sqrt(square(r) / f))
        delta = 2 * n * d * cos(i)
        k = pi * delta / lamda

        I0 = square(cos(k))

        I = I0[:, int(N/2)]

        self.imgdata = I0

        # 生成对应波长的色矩
        my_cmap = wavelength_to_map(self.SpinBox_lamda.value())
        self.my_cmp = my_cmap


        # 创建衍射图像
        mpl = self.mplwidget_diffraction.canvas
        # 清除当前图像
        mpl.ax.clear()
        # 设置图像参数
        mpl.ax.imshow( 2 * I0, cmap=my_cmap, interpolation='bessel', origin='lower', vmin=0, vmax=1)
        mpl.ax.axis('off')  # 去掉坐标轴
        mpl.draw()  # 显示

        # 光强分布图像
        axes = self.mplwidget_I.canvas.ax
        fig = self.mplwidget_I.canvas.fig
        axes.cla()
        # 设置图像参数
        axes.plot(x, I, color=my_cmap.colors[-1], linewidth=1.5)
        # 设置x轴
        axes.set_xlabel('X(m)', self.font)
        # 设置y轴
        axes.set_ylabel('I', self.font)
        labels = axes.get_xticklabels() + axes.get_yticklabels()
        [label.set_fontname('Times New Roman') for label in labels]
        # 设置图像标题
        # fig.suptitle('光强分布', fontweight='bold', fontproperties=self.SongTi, fontsize=26, )
        fig.canvas.draw()  # 显示图像
        fig.canvas.flush_events()  # 刷新图像 否则会不更新






    # @ pyqtSlot("double")
    # def on_SpinBox_a_valueChanged(self):
    #     self.fig()

    @pyqtSlot("double")
    def on_SpinBox_x_valueChanged(self):
        self.fig()

    @pyqtSlot("double")
    def on_SpinBox_d_valueChanged(self):
        self.fig()

    @pyqtSlot("double")
    def on_SpinBox_R_valueChanged(self):
         self.fig()

    @pyqtSlot("double")
    def on_SpinBox_f_valueChanged(self):
        self.fig()

    @pyqtSlot("int")
    def on_SpinBox_N_valueChanged(self):
        self.fig()

    @pyqtSlot("double")
    def on_SpinBox_n_valueChanged(self):
        self.fig()

    @pyqtSlot("double")
    def on_SpinBox_lamda_valueChanged(self):
        self.fig()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyApplication = MainApp()
    MyApplication.showFullScreen()
    sys.exit(app.exec())