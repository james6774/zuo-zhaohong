import re
import pandas as pd
import os

path = ".\\save\\"

import os
dbtype_list = os.listdir(path)
for dbtype in dbtype_list:
    if os.path.isfile(os.path.join(path,dbtype)):
        dbtype_list.remove(dbtype)
#print("请输入你保存的文件的名称：",end=" ")
#path_1= input()
name = []
## 读取文件
for dbtype in dbtype_list:
    f = open(path +dbtype+ '\\species.out.txt','r')
    csv = re.split('\n',f.read())
    f.close()
    ##总结果，dict形式{'H20':1}的列表
    list_result = []

    try:
        for x,i in enumerate(csv):
            ## 取化学式字段
            if x%2==0:
                result = re.split('\s',i)
                # 取出字段中的化学式
                result = [m for m in result if m!='' and m!='#']
                # 放在一个总列表中，以此作为表头
                name += [m for m in result if m not in name]
                number = re.split('\s',csv[x+1])
                # 取组分
                number = [m for m in number if m.isdigit()]
                # 构建字典
                list_result.append(dict(zip(result, number)))
    except:
        pass

    nn = [0 for _ in range((len(name)))]
    ttt = []
    for i in list_result:
        result = dict(zip(name, nn))
        for x in i.keys():
            # 有则替代表中dict的值
            result[x] = i[x]
        ttt.append(list(result.values()))  # 修改这行
    df = pd.DataFrame([name] + ttt )
    # 生成文件
    df.to_csv(path+dbtype + '\\result.csv')
    print(df)
