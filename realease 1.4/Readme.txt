欢迎使用聚合物裂解模拟计算实验GUI！

这是基于python语言并运用pyqt5库开发的GUI，所以在运行前需确保您的电脑安装了python以及pyqt5
开发者给用户提供了python3.9的安装包，python的安装具体请参考以下CSDN文章：
https://blog.csdn.net/m0_59162248/article/details/128047979?ops_request_misc=&request_id=&biz_id=102&utm_term=python%E4%B8%8B%E8%BD%BD%E5%9C%B0%E5%9D%80&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-128047979.nonecase&spm=1018.2226.3001.4187

安装好python之后，打开命令提示符（cmd），输入python --version，如果有信息出现，则说明python安装成功。
接下来继续在命令提示符（cmd）中输入pip install pyqt5，即可安装pyqt5
安装完成之后，再次使用命令提示符（cmd）并cd进入到程序目录下，输入python Main.py即可启动GUI





请按照以下步骤进行操作：


请在开始计算之前先安装lammps模拟软件Windows系统并行版，这里开发者提供了一个lammps安装包和一个MPICH安装包，注意，这两个软件必须同时安装才能正常使用，如果需要其他版本，可自行前往软件官网进行下载
lammps与MPICH2的官网下载地址都在此处：
https://packages.lammps.org/windows.html
详细安装方法可参考以下两篇CSDN文章：
https://blog.csdn.net/m0_60787307/article/details/124075394?ops_request_misc=&request_id=&biz_id=102&utm_term=lammpswindows%E5%AE%89%E8%A3%85%E6%95%99%E7%A8%8B&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-2-124075394.142^v83^insert_down38,239^v2^insert_chatgpt&spm=1018.2226.3001.4187

https://blog.csdn.net/weixin_43592490/article/details/115470519?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522168171633016800184136502%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=168171633016800184136502&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~baidu_landing_v2~default-2-115470519-null-null.142^v83^insert_down38,239^v2^insert_chatgpt&utm_term=lammps%20Windows%E7%89%88%E6%9C%AC%E5%AE%89%E8%A3%85&spm=1018.2226.3001.4187

注1：以上软件安装之后都要添加环境变量，否则可能无法正常使用
注2：如果只安装了lammps，没有安装MPICH2，GUI可能会在开始计算时报错闪退



第一步：创建模型文件
	输入账号密码登录，登陆成功后，将在程序目录下创建一个以账号为名的文件夹。
	在选择模型一栏中，开发者为用户提供了三个简单的模型文件，即聚合度为60的聚乙烯（PE）、聚丁二烯（PB）和聚乙烯醇（PVA），选中所需的模型后，点击”确定“来导入模型文件、in文件和力场文件。如果这三种模型不符合您的需求，您可以点击“导入自建模型”，选择您计算机中自建的模型文件（原子坐标文件）来进行导入。
	注：这些计算的所需文件都会导入登录时以账号为名的文件夹中，当完成一次计算并保存所需要的结果后，在导入新的模型文件之前，您需要点击“清空”来删除此文件夹中的缓存文件，以免导入新的模型文件之后造成文件混乱影响计算结果。

第二步：查看、修改相关参数
	在创建模型文件之后，点击”参数修改“进入到下一栏，这里可以查看刚导入的三种文件，并可根据自身需要修改对应参数并保存。
	注1：每次导入一个新模型时，所有相关参数都会恢复至默认参数，如有需要，请记得修改
	注2：如果导入的是自建模型，需要在read_data处输入您所导入原子坐标文件的名称，否则在点击”开始计算“之后，会出现计算出错的结果。

第三步：计算
	完成前两步后，点击“计算”进入到计算页面，点击“开始计算”后调用lammps进行计算，计算完成后会有弹窗提示计算完成，请耐心等待。
	注1：开发者使用的lammps启动计算命令为“lmp < in.lmp.txt”，如果与您的lammps启动命令不同或是想使用多核并行计算，请在确认您的计算机安装了相关组件之后，修改Main.py的381行处
self.lammps_process = subprocess.Popen('lmp < in.lmp.txt', shell=True) 的lammps启动命令代码，例如修改为
self.lammps_process = subprocess.Popen('mpiexec -n 4 lmp < in.lmp.txt', shell=True) 意为调用4个cpu核进行运算
	注2：如果加上mpiexec命令后lammps计算出错，可能是使用该命令是报错：
	Credentials for XXX rejected connecting to YYY
	Aborting: Unable to connect to YYY
	其中，XXX是用户的安装MPIC2时注册的用户名，YYY是用户的设备名称。
	其具体解决方法因个人而异，请用户自行查询相关资料以解决。

第四步：结果预览与保存
	计算完成后，进入到“结果预览“一栏，在这里可以查看分子运动轨迹文件以及物种文件，或者在计算的过程中，您也可以打开物种文件以查看计算进行的进度，如果需要保留计算结果，点击”保存“，然后自定义保存文件夹的名称，即可将计算结果保存到程序目录下的save文件夹中。
	注1：需要在启动GUI之前，将.CHO后缀文件的默认启动程序设置为Ovito，才能在GUI中直接打开分子运动轨迹文件。若未设置默认启动程序，只能将计算结果保存之后，把dump.CHO文件拖到Ovito之中才能打开。
	注2：在开始一个新的计算之后或是点击了”选择模型“一栏中的”清空“之后，上一次的计算结果都会自动删除，如需保留请记得及时保存。