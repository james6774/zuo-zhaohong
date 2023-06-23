import os
import shutil
import subprocess
import sys
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, \
    QLabel, QMessageBox, QLineEdit, QFileDialog
from LoginUi import *
from InterfaceUi import *

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(15)
        self.shadow.setColor(QtCore.Qt.black)
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.ui.pushButton_L_sure.clicked.connect(self.login_in)
        self.ui.pushButton.setIcon(QIcon("IMG/close.png"))
        self.setWindowIcon(QIcon("IMG/LIMG.png"))
        self.show()

    def login_in(self):
        account = self.ui.lineEdit_L_account.text()
        password = self.ui.lineEdit_L_password.text()
        if account == '' or password == '':
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            # 创建一个以账号命名的文件夹
            dir_path = os.path.join(os.getcwd(), account)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            # 弹出登录成功的提示框
            QMessageBox.information(self, "提示", "登陆成功，欢迎进行聚合物裂解模拟计算实验", QMessageBox.Ok)
            # 进入空白界面
            MainWindow(dir_path).show()
            self.close()


class MainWindow(QMainWindow):
    def __init__(self, dir_path):
        super().__init__()
        self.destination_folder = dir_path
        self.source_file1 = None
        self.source_file2 = None
        self.source_file3 = None
        self.lammps_process = None
        self.thread = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_home.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.button1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.button2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.button3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.button4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("IMG/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_close.setIcon(icon)
        icon_1 = QtGui.QIcon()
        icon_1.addPixmap(QtGui.QPixmap("IMG/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.pushButton_min.setIcon(icon_1)
        icon_2 = QtGui.QIcon()
        icon_2.addPixmap(QtGui.QPixmap("IMG/LIMG.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QIcon("IMG/LIMG.png"))
        self.ui.pushButton_8.setIcon(icon_2)
        self.ui.pe_button.clicked.connect(lambda: self.select_file("PE"))
        self.ui.pb_button.clicked.connect(lambda: self.select_file("PB"))
        self.ui.pva_button.clicked.connect(lambda: self.select_file("PVA"))
        self.ui.clear_button.clicked.connect(self.clear)
        self.ui.other_button.clicked.connect(self.others)
        self.ui.next_button.clicked.connect(self.copy_file)
        self.ui.pushButton_1.clicked.connect(self.Data)
        self.ui.pushButton_2.clicked.connect(self.In)
        self.ui.pushButton_3.clicked.connect(self.Ffield)
        self.ui.pushButton_4.clicked.connect(self.start_computation)
        self.ui.pushButton_5.clicked.connect(self.Dump)
        self.ui.pushButton_6.clicked.connect(self.Species)
        self.ui.pushButton_7.clicked.connect(self.Save)
        self.ui.button5.clicked.connect(self.back)
        self.ui.button6.clicked.connect(self.help)

    def select_file(self, model):
        if model == "PE":
            self.ui.pb_button.setStyleSheet("border:2px solid black; border-radius:7px;")
            self.ui.pva_button.setStyleSheet("border:2px solid black; border-radius:7px;")
            self.ui.pe_button.setStyleSheet("background-color: green")
            self.source_file1 = './data/PE/data.CHO.txt'
            self.source_file2 = './in/in.lmp.txt'
            self.source_file3 = './tools/ffield.reax.cho.txt'
            pixmap = QPixmap('./model/PE.png')
            pixmap = pixmap.scaledToWidth(380)
            self.ui.image_label.setPixmap(pixmap)

        elif model == "PB":
            self.ui.pe_button.setStyleSheet("border:2px solid black; border-radius:7px;")
            self.ui.pva_button.setStyleSheet("border:2px solid black; border-radius:7px;")
            self.ui.pb_button.setStyleSheet("background-color: green")
            self.source_file1 = './data/PB/data.CHO.txt'
            self.source_file2 = './in/in.lmp.txt'
            self.source_file3 = './tools/ffield.reax.cho.txt'
            pixmap = QPixmap('./model/PB.png')
            pixmap = pixmap.scaledToWidth(380)
            self.ui.image_label.setPixmap(pixmap)

        elif model == "PVA":
            self.ui.pe_button.setStyleSheet("border:2px solid black; border-radius:7px;")
            self.ui.pb_button.setStyleSheet("border:2px solid black; border-radius:7px;")
            self.ui.pva_button.setStyleSheet("background-color: green")
            self.source_file1 = './data/PVA/data.CHO.txt'
            self.source_file2 = './in/in.lmp.txt'
            self.source_file3 = './tools/ffield.reax.cho.txt'
            pixmap = QPixmap('./model/PVA.png')
            pixmap = pixmap.scaledToWidth(380)
            self.ui.image_label.setPixmap(pixmap)

    def clear(self):
        folder_path = self.destination_folder  # 指定要删除的文件夹路径

        # 删除文件夹下的所有文件
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        QMessageBox.information(self, "清空", "文件已清空", QMessageBox.Ok)

    def others(self):
        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件')

        if file_path:
            # 选择保存路径
            save_dir = self.destination_folder

            if save_dir:
                # 复制文件
                file_name = os.path.basename(file_path)
                save_path = os.path.join(save_dir, file_name)
                in_dir = './in/others/in.lmp.txt'
                ffield_dir = './tools/ffield.reax.cho.txt'
                shutil.copy(in_dir, self.destination_folder)
                shutil.copy(ffield_dir, self.destination_folder)
                try:
                    with open(file_path, 'rb') as src_file, open(save_path, 'wb') as dst_file:
                        dst_file.write(src_file.read())
                    QMessageBox.information(self, "加载", "模型文件导入成功", QMessageBox.Ok)
                except:
                    QMessageBox.warning(self, "加载", "模型文件导入失败", QMessageBox.Ok)

    def copy_file(self):
        if self.source_file1 is None:
            QMessageBox.warning(self, "警告", "请选择一个模型", QMessageBox.Ok)
        else:
            if self.source_file1 and self.destination_folder:
                shutil.copy(self.source_file1, self.destination_folder)
                shutil.copy(self.source_file2, self.destination_folder)
                shutil.copy(self.source_file3, self.destination_folder)
                QMessageBox.information(self, "加载", "模型文件导入成功", QMessageBox.Ok)

    def Data(self):
        current_dir = os.getcwd()

        # 定义要打开的文件路径（相对路径）
        file_path1 = self.destination_folder + '/data.CHO.txt'

        # 使用Notepad打开文件
        if file_path1:
            try:
                os.startfile(os.path.join(current_dir, file_path1))
            except FileNotFoundError:
                QMessageBox.warning(self, '警告', '模型尚未被创建')

    def In(self):
        current_dir = os.getcwd()

        # 定义要打开的文件路径（相对路径）
        file_path2 = self.destination_folder + '/in.lmp.txt'

        # 使用Notepad打开文件
        if file_path2:
            try:
                os.startfile(os.path.join(current_dir, file_path2))
            except FileNotFoundError:
                QMessageBox.warning(self, '警告', '模型尚未被创建')

    def Ffield(self):
        current_dir = os.getcwd()

        # 定义要打开的文件路径（相对路径）
        file_path3 = self.destination_folder + '/ffield.reax.cho.txt'

        # 使用Notepad打开文件
        if file_path3:
            try:
                os.startfile(os.path.join(current_dir, file_path3))
            except FileNotFoundError:
                QMessageBox.warning(self, '警告', '模型尚未被创建')

    def start_computation(self):
        try:
            # 检查 lmp 命令是否在系统路径中
            subprocess.run(['lmp', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except FileNotFoundError:
            # 如果找不到 lmp 命令，则弹出一个消息框提示用户未安装 LAMMPS
            QMessageBox.warning(self, 'Lammps计算', '尚未安装 LAMMPS，请先安装。', QMessageBox.Ok)
            return

        input_file = os.path.join(self.destination_folder, 'in.lmp.txt')
        if not os.path.exists(input_file):
            QMessageBox.warning(self, 'Lammps计算', '模型尚未被创建。', QMessageBox.Ok)
            return

        if self.lammps_process is not None and self.lammps_process.poll() is None:
            # 如果当前已经有一个lammps进程正在运行，则弹出一个消息框提醒用户等待计算完成
            QMessageBox.warning(self, 'Lammps计算', '当前已有一个计算正在进行，请等待计算完成后再尝试。', QMessageBox.Ok)
        else:
            # 检查是否已经有一个计算线程正在运行
            if getattr(self, 'thread', None) and self.thread.isRunning():
                # 如果有，则不启动新的计算线程
                QMessageBox.warning(self, 'Lammps计算', '当前已有一个计算正在进行，请等待计算完成后再尝试。', QMessageBox.Ok)
                return
            else:
                # 否则，启动一个新的线程进行计算
                self.thread = ComputeThread(self.destination_folder)
                self.thread.finished.connect(self.on_computation_finished)
                self.thread.start()

    def on_computation_finished(self):
        input_file = os.path.join(self.destination_folder, 'dump.CHO')
        if not os.path.exists(input_file):
            QMessageBox.warning(self, 'Lammps计算', '计算出错', QMessageBox.Ok)
            return
        QMessageBox.information(self, 'Lammps计算', '计算已经完成。', QMessageBox.Ok)  # 在计算完成后弹出消息框

    def Dump(self):
        input_file = os.path.join(self.destination_folder, 'dump.CHO')
        if not os.path.exists(input_file):
            QMessageBox.warning(self, '未找到文件', '尚未进行计算。', QMessageBox.Ok)
            return

        current_dir = os.getcwd()

        # 定义要打开的文件路径（相对路径）
        file_path1 = self.destination_folder + '/dump.CHO'

        # 使用Notepad打开文件
        try:
            os.startfile(os.path.join(current_dir, file_path1))
        except WindowsError:
            QMessageBox.warning(self, "警告", "没有指定默认应用程序。", QMessageBox.Ok)

    def Species(self):
        current_dir = os.getcwd()

        # 定义要打开的文件路径（相对路径）
        file_path2 = self.destination_folder + '/species.out.txt'

        # 使用Notepad打开文件
        try:
            os.startfile(os.path.join(current_dir, file_path2))
        except FileNotFoundError:
            QMessageBox.warning(self, '警告', '尚未进行计算')

    def Save(self):
        input_file = os.path.join(self.destination_folder, 'dump.CHO')
        if not os.path.exists(input_file):
            QMessageBox.warning(self, '未找到文件', '尚未进行计算。', QMessageBox.Ok)
            return

        folder_path = self.destination_folder
        self.save_window = SaveWindow(folder_path)
        self.save_window.show()

    def back(self):
        self.back_window = LoginWindow()
        self.back_window.show()
        self.close()

    def help(self):
        os.startfile('Readme.txt')


class ComputeThread(QThread):
    finished = pyqtSignal()  # 线程完成信号

    def __init__(self, dir_path):
        super().__init__()
        self.destination_folder = dir_path
        self.successful = False  # 添加计算成功标志

    def run(self):
        dir_path = self.destination_folder
        os.chdir(os.path.join('.', dir_path))
        try:
            self.lammps_process = subprocess.Popen('lmp < in.lmp.txt', shell=True)
            self.lammps_process.wait()  # 等待LAMMPS进程完成
            self.successful = True  # 计算成功
        except subprocess.CalledProcessError:
            self.successful = False  # 计算异常终止
        finally:
            # 获取当前工作目录的绝对路径
            current_dir = os.getcwd()

            # 获取程序根目录的绝对路径
            root_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

            # 返回程序根目录
            os.chdir(root_dir)

        if self.successful:  # 如果计算成功，则发送完成信号
            self.finished.emit()  # 发送完成信号
        else:
            QMessageBox.warning(self, 'Lammps计算', '计算出错', QMessageBox.Ok)
            return


class SaveWindow(QWidget):
    def __init__(self, folder_path):
        super().__init__()
        self.destination_folder = folder_path
        self.setWindowTitle("设置保存文件夹的名称")
        self.setGeometry(760, 475, 400, 150)

        # 创建QLabel
        self.label = QLabel("设置保存文件夹的名称：")

        # 创建QLineEdit
        self.line_edit = QLineEdit()

        # 创建QPushButton
        self.button = QPushButton("确定")
        self.button.clicked.connect(self.on_button_click)

        # 创建垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

        # 将布局设置为主窗口的布局
        self.setLayout(layout)

    def on_button_click(self):
        file_path1 = self.destination_folder + '/dump.CHO'
        file_path2 = self.destination_folder + '/species.out.txt'
        save_name = self.line_edit.text()
        save_path = os.path.join('./save', save_name)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        shutil.copy(file_path1, save_path)
        shutil.copy(file_path2, save_path)
        QMessageBox.information(self, "提示", "保存成功", QMessageBox.Ok)
        self.close()

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    app.exec_()
    