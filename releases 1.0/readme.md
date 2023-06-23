## 聚合物裂解模拟计算实验

本项目是一个基于PyQt5的调用Lammps进行计算的项目

### 快速开始

安装[lammps](https://packages.lammps.org/windows.html)

（可选）安装[MPICH](https://www.mpich.org/)

（可选）安装[Ovito](https://www.ovito.org/windows-downloads)

（可选）[python免安装包](https://www.123pan.com/s/fu7eVv-pO2PH.html)（将其覆盖在根目录）

命名行运行

```
git clone 
cd Polymer_cracking
#未使用python免安装包
pip install -r requirements.txt
python main.py
#使用python免安装包
./run.bat #直接点击也行
```

### 使用

#### #### 载入模型

- 输入账号密码登录

- 有三个模型分别为聚合度为60的聚乙烯（PE）、聚丁二烯（PB）和聚乙烯醇（PVA）

- 选中任一模型，载入

- 如果想自建模型也可以点击“导入自建模型”

#### 计算

- 点击计算按钮，开始计算，调用lammps进行计算

- 本项目中默认会不使用使用MPICH进行多核加速，如安装MPICH，想使用多核进行加速，可将Main.py的387行处

```python
self.lammps_process = subprocess.Popen('lmp < in.lmp.txt', shell=True) 
```

- 改为（本句为使用MPICH进行四核计算）

```python
self.lammps_process = subprocess.Popen('mpiexec -n 4 lmp < in.lmp.txt', shell=True) 
```

- 以进行多核加速

#### 结果

- 计算完成后，进入到“结果预览“一栏，在这里可以查看分子运动轨迹文件以及物种文件，或者在计算的过程中，

- 也可以打开物种文件以查看计算进行的进度，如果需要保留计算结果，点击”保存“，然后自定义保存文件夹的名称，即可将计算结果保存到程序目录下的save文件夹中。

- .CHO后缀文件需要Ovito来使用

- 如需要转为csv的物种文件，可点击“species文件转为csv文件”
