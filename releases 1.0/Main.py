import os
import shutil
import subprocess
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStackedWidget, QVBoxLayout, QHBoxLayout, QSplitter, \
    QLabel, QMessageBox, QDesktopWidget, QLineEdit, QFileDialog


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口大小
        self.resize(400, 300)
        self.setWindowTitle('登录')

        # 设置所有控件居中显示
        self.welcome_label = QLabel("聚合物裂解模拟计算实验")
        self.welcome_label.setFont(QFont('SansSerif', 18))
        self.account_label = QLabel("账号:")
        self.account_label.setFont(QFont('SansSerif', 18))
        self.password_label = QLabel("密码:")
        self.password_label.setFont(QFont('SansSerif', 18))
        self.account_edit = QLineEdit()
        self.account_edit.setFont(QFont('SansSerif', 18))
        self.password_edit = QLineEdit()
        self.password_edit.setFont(QFont('SansSerif', 18))
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.login)
        self.exit_button = QPushButton("退出")
        self.exit_button.clicked.connect(self.close)

        # 设置布局
        vbox = QVBoxLayout()
        hbox0 = QHBoxLayout()
        hbox0.addStretch(1)
        hbox0.addWidget(self.welcome_label)
        hbox0.addStretch(1)
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.account_label)
        hbox1.addWidget(self.account_edit)
        hbox1.addStretch(1)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.password_label)
        hbox2.addWidget(self.password_edit)
        hbox2.addStretch(1)
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.login_button)
        hbox3.addWidget(self.exit_button)
        hbox3.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # 设置窗口居中显示
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def login(self):
        account = self.account_edit.text()
        password = self.password_edit.text()
        if account == '' or password == '':
            QMessageBox.warning(self, "警告", "账号或密码不能为空", QMessageBox.Ok)
        else:
            # 创建一个以账号命名的文件夹
            dir_path = os.path.join(os.getcwd(), account)
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            # 弹出登录成功的提示框
            QMessageBox.information(self, "提示", "登陆成功，欢迎进行聚合物裂解模拟计算实验", QMessageBox.Ok)
            # 进入空白界面
            self.next_window = MainWindow(dir_path)
            self.next_window.show()
            self.close()

class MainWindow(QWidget):
    def __init__(self, dir_path):
        super().__init__()
        self.destination_folder = dir_path
        self.initUI()

    def initUI(self):
        button1 = QPushButton("选择模型", self)
        button1.setFixedSize(100, 60)
        button1.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        button2 = QPushButton("参数修改", self)
        button2.setFixedSize(100, 60)
        button2.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        button3 = QPushButton("计算", self)
        button3.setFixedSize(100, 60)
        button3.clicked.connect(lambda: stacked_widget.setCurrentIndex(2))
        button4 = QPushButton("结果预览", self)
        button4.setFixedSize(100, 60)
        button4.clicked.connect(lambda: stacked_widget.setCurrentIndex(3))
        button5 = QPushButton("注销", self)
        button5.setFixedSize(100, 60)
        button5.clicked.connect(self.back)
        button6 = QPushButton("使用帮助", self)
        button6.setFixedSize(100, 60)
        button6.clicked.connect(self.help)

        vlayout = QVBoxLayout()
        vlayout.addWidget(button1)
        vlayout.addWidget(button2)
        vlayout.addWidget(button3)
        vlayout.addWidget(button4)
        vlayout.addWidget(button5)
        vlayout.addWidget(button6)

        stacked_widget = QStackedWidget()
        stacked_widget.setFixedSize(800, 600)

        dir_path = self.destination_folder
        widget1 = SelectModel(dir_path)
        widget2 = SelectIn(dir_path)
        widget3 = Compute(dir_path)
        widget4 = Result(dir_path)
        stacked_widget.addWidget(widget1)
        stacked_widget.addWidget(widget2)
        stacked_widget.addWidget(widget3)
        stacked_widget.addWidget(widget4)

        # 将左右区域组合到一起
        splitter = QSplitter()
        splitter.addWidget(QWidget())
        splitter.addWidget(stacked_widget)
        splitter.setSizes([1, 4])

        # 创建一个水平布局并将左侧垂直布局和右侧QStackedWidget添加到其中
        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayout)
        hlayout.addWidget(splitter)

        # 设置整个窗口的布局为水平布局
        self.setLayout(hlayout)

        # 设置窗口大小为1000x600
        self.setFixedSize(1000, 600)
        self.setWindowTitle('聚合物裂解模拟计算实验')

        self.page_list = [widget1, widget2, widget3, widget4]
        self.current_page = 0

    def back(self):
        self.back_window = LoginWindow()
        self.back_window.show()
        self.close()

    def help(self):
        os.startfile('Readme.txt')

class SelectModel(QWidget):
    def __init__(self, dir_path):
        super().__init__()
        self.destination_folder = dir_path
        self.source_file1 = None
        self.source_file2 = None
        self.source_file3 = None

        # 设置窗口大小
        self.resize(800, 600)

        # 设置所有控件居中显示
        choose_label = QLabel("选择你所需要的模型")
        choose_label.setFont(QFont('SansSerif',18))
        self.pe_button = QPushButton("PE")
        self.pe_button.clicked.connect(lambda: self.select_file("PE"))
        self.pb_button = QPushButton("PB")
        self.pb_button.clicked.connect(lambda: self.select_file("PB"))
        self.pva_button = QPushButton("PVA")
        self.pva_button.clicked.connect(lambda: self.select_file("PVA"))
        self.image_label = QLabel()
        self.image_label.setFixedSize(400, 400)

        # 设置布局
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(choose_label, alignment=Qt.AlignCenter)
        vbox.addStretch(1)
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.pe_button)
        hbox1.addWidget(self.pb_button)
        hbox1.addWidget(self.pva_button)
        hbox1.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.image_label)
        hbox2.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        clear_button = QPushButton("清空")
        other_button = QPushButton("导入自建模型")
        next_button = QPushButton("确定")
        next_button.clicked.connect(self.copy_file)
        other_button.clicked.connect(self.others)
        clear_button.clicked.connect(self.clear)
        hbox3.addWidget(clear_button)
        hbox3.addWidget(other_button)
        hbox3.addWidget(next_button)
        hbox3.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        self.setLayout(vbox)

        # 设置窗口居中显示
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def select_file(self, model):
        if model == "PE":
            self.pb_button.setStyleSheet("background-color: white")
            self.pva_button.setStyleSheet("background-color: white")
            self.pe_button.setStyleSheet("background-color: green")
            self.source_file1 = './data/PE/data.CHO.txt'
            self.source_file2 = './in/in.lmp.txt'
            self.source_file3 = './tools/ffield.reax.cho.txt'
            pixmap = QPixmap('./model/PE.png')
            pixmap = pixmap.scaledToWidth(400)
            self.image_label.setPixmap(pixmap)

        elif model == "PB":
            self.pe_button.setStyleSheet("background-color: white")
            self.pva_button.setStyleSheet("background-color: white")
            self.pb_button.setStyleSheet("background-color: green")
            self.source_file1 = './data/PB/data.CHO.txt'
            self.source_file2 = './in/in.lmp.txt'
            self.source_file3 = './tools/ffield.reax.cho.txt'
            pixmap = QPixmap('./model/PB.png')
            pixmap = pixmap.scaledToWidth(400)
            self.image_label.setPixmap(pixmap)

        elif model == "PVA":
            self.pe_button.setStyleSheet("background-color: white")
            self.pb_button.setStyleSheet("background-color: white")
            self.pva_button.setStyleSheet("background-color: green")
            self.source_file1 = './data/PVA/data.CHO.txt'
            self.source_file2 = './in/in.lmp.txt'
            self.source_file3 = './tools/ffield.reax.cho.txt'
            pixmap = QPixmap('./model/PVA.png')
            pixmap = pixmap.scaledToWidth(400)
            self.image_label.setPixmap(pixmap)

    def copy_file(self):
        if self.source_file1 is None:
            QMessageBox.warning(self, "警告", "请选择一个模型", QMessageBox.Ok)
        else:
            if self.source_file1 and self.destination_folder:
                shutil.copy(self.source_file1, self.destination_folder)
                shutil.copy(self.source_file2, self.destination_folder)
                shutil.copy(self.source_file3, self.destination_folder)
                QMessageBox.information(self, "加载", "模型文件导入成功", QMessageBox.Ok)

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

class SelectIn(QWidget):
    def __init__(self, dir_path):
        super().__init__()
        self.destination_folder = dir_path

        # 设置窗口大小为800x600
        self.setGeometry(100, 100, 800, 600)

        self.button1 = QPushButton('原子坐标文件（data文件）', self)
        self.button1.setGeometry(200, 50, 400, 50)
        self.button1.clicked.connect(self.Data)

        self.button2 = QPushButton('控制文件（In文件）', self)
        self.button2.setGeometry(200, 250, 400, 50)
        self.button2.clicked.connect(self.In)

        self.button3 = QPushButton('力场文件（ffield文件）', self)
        self.button3.setGeometry(200, 450, 400, 50)
        self.button3.clicked.connect(self.Ffield)

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

class Compute(QWidget):
    def __init__(self, dir_path):
        super().__init__()
        self.destination_folder = dir_path
        self.lammps_process = None
        self.thread = None

        # 设置窗口大小为800x600
        self.setGeometry(100, 100, 800, 600)

        self.button1 = QPushButton('开始计算', self)
        self.button1.setGeometry(200, 250, 400, 100)
        self.button1.clicked.connect(self.start_computation)

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

class Result(QWidget):
    def __init__(self, dir_path):
        super().__init__()
        self.destination_folder = dir_path

        # 设置窗口大小为800x600
        self.setGeometry(100, 100, 800, 600)

        self.button1 = QPushButton('查看分子运动轨迹（dump文件）', self)
        self.button1.setGeometry(200, 50, 400, 50)
        self.button1.clicked.connect(self.Dump)

        self.button2 = QPushButton('查看物种文件（species文件）', self)
        self.button2.setGeometry(200, 200, 400, 50)
        self.button2.clicked.connect(self.Species)

        self.button3 = QPushButton('保存结果', self)
        self.button3.setGeometry(200, 350, 400, 50)
        self.button3.clicked.connect(self.Save)

        self.button4 = QPushButton('species文件转为csv', self)
        self.button4.setGeometry(200, 500, 400, 50)
        self.button4.clicked.connect(self.translate)

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
    def translate(self):
        os.system("python species_analysis.py")

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
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    app.exec_()