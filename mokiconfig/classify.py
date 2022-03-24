# 文件分类器，将文件自动分类
'''
为了便于代码说明，及配置方便。对文件或文件夹的名称的各部分起称呼
例如：
a@book.jpeg
说明：
a@book:文件名
a：意图文件名
@book：分类规则
@：分类标识符
book：分类标识名
.jpeg:扩展名

例如
a@rm@txt@book.jpeg
说明：从后向前
@book：一阶分类规则
book：一阶分类标识名
@txt：二阶分类规则
txt：二阶分类标识名
@rm：三阶分类规则
rm:三阶分类标识名

程序默认按照一阶分类规则进行分类
'''
import os
import xlrd
import xlwt
import shutil

def readConfig():	# 读取配置文件
	global config, modeConfig, functionConfig, status, mode, signal, root	# 定义为全局变量
	config = xlrd.open_workbook(r'./config.xls')	# 读取配置文件
	modeConfig = config.sheet_by_name('rule')	# 读取规则表
	functionConfig = config.sheet_by_name('function')	# 读取功能表

	status = modeConfig.cell(0,1).value	# 启用状态
	mode = modeConfig.cell(1,1).value	# 分类模式
	signal = modeConfig.cell(2,1).value	# 读取分类标识符
	root = modeConfig.cell(3,1).value	# 聚合目录，将分类好的文件放入此文件夹
	
	readOrder()	

def readOrder():	# 读取指令
	global mvDic	# 定义为全局遍历
	mvDic = {}	# 分类标识字典
	nrows = functionConfig.nrows
	for i in range(1,nrows):
		if functionConfig.cell(i,0).value == "mv":	# 功能为分类
			mvDic[functionConfig.cell(i,1).value] = functionConfig.cell(i,2).value

	os.chdir("../../")	# 改变工作目录,为运行文件的上上一级目录

def mv():	# 无论是文件还是目录都移动
	for file in os.listdir():	# 列出目录下的所有文件及文件夹名称	1@img.jpeg
		filename = os.path.splitext(file)[0]	# 文件名	1@img
		suffix = filename.split(signal)[-1]	# 分类标识名	img
		dirname = mvDic.get(suffix, 0)	# img -> 图片
		if dirname != 0:	# 存在此键值对
			if not os.path.exists(dirname):	# 判断是否有文件夹，没有则创建
				os.mkdir(dirname)	# 创建文件夹 图片
			shutil.move(file, dirname)	# 将文件移动到文件夹中

# 保留可供选择使用
def mvFile():	# 只移动文件
	for file in os.listdir():
		if(os.path.isfile(file)):	# 是文件
			filename = os.path.splitext(file)[0]	# 文件名
			suffix = filename.split(signal)[-1]
			dirname = mvDic[suffix]
			if not os.path.exists(dirname):	# 判断是否有文件夹，没有则创建
				os.mkdir(dirname)
			shutil.move(file, dirname)
			

# 保留可供选择使用
def mvDir():	# 只移动目录及其目录下的文件
	for file in os.listdir():
		if(os.path.isdir(file)):	# 是目录
			filename = os.path.splitext(file)[0]	# 文件名
			suffix = filename.split(signal)[-1]
			dirname = mvDic.get(suffix, 0)#mvDic[suffix]
			if dirname != 0:
				if not os.path.exists(dirname):	# 判断是否有文件夹，没有则创建
					os.mkdir(dirname)
				shutil.move(file, dirname)	#递归地将一个文件或目录 (src) 移至另一位置 (dst) 并返回目标位置

# 去除已分类的分类规则（不对未分类的处理），文件夹（不含其内的子文件）和文件
def throwSuffix():
	for item in mvDic.items():	# 遍历字典中的元组(键，值)
		if os.path.exists(item[1]):	#检查是否存在此目录
			for file in os.listdir(item[1]):	# 获取值
				filename = os.path.splitext(file)[0]	# 文件名 a@img
				suffix = filename.split(signal)[-1]	# 分类标识名 img
				dirname = mvDic.get(suffix, 0)	# img -> 图片
				if dirname != 0:
					os.chdir(item[1])	# 改变工作目录
					if(os.path.isfile(file)):	# 是文件
						filesuffix = os.path.splitext(file)[1]	# 扩展名 .jpeg
						midname = signal.join(filename.split('@')[0:-1])	# 去除一阶分类规则
						newname = midname + filesuffix	# 拼接意图文件名和扩展名
						shutil.move(file, newname)	# 重命名
					elif(os.path.isdir(file)):	# 是目录
						newname = signal.join(filename.split('@')[0:-1])	# 去除一阶分类规则
						shutil.move(file, newname)	# 重命名
					os.chdir("../")	# 改变工作目录

# 恢复分类规则
def resumeSuffix():
	for item in mvDic.items():	# 遍历字典中的元组(键，值)
		if os.path.exists(item[1]):
			for file in os.listdir(item[1]):
				filename = os.path.splitext(file)[0]	# 意图文件名 a
				os.chdir(item[1])	# 改变工作目录
				if(os.path.isfile(file)):	# 是文件
					filesuffix = os.path.splitext(file)[1]	# 扩展名 .jpeg
					newname = filename + signal + item[0] + filesuffix	# 拼接 意图文件名 + 分类标识符 + 分类标识名 + 扩展名
					shutil.move(file, newname)	# 重命名
				elif(os.path.isdir(file)):	# 是目录
					newname = filename + signal + item[0]
					shutil.move(file, newname)	# 重命名
				os.chdir("../")	# 改变工作目录


if __name__ == '__main__':
	readConfig()
	if status == 1:	# 启用分类器
		if mode == 1:	# 分类模式1，分类所有文件及文件夹
			mv()
		elif mode == 3:
			throwSuffix()	# 分类模式2，去除所有分类规则
		elif mode == 4:
			resumeSuffix()	# 分类模式3，恢复所有分类规则