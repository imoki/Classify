# 文件分类器，将文件自动分类
import os
import xlrd
import xlwt
import shutil

def readConfig():	# 读取配置文件
	global config, modeConfig, functionConfig, status, mode, signal, root	# 定义为全局变量
	config = xlrd.open_workbook(r'./config.xls')
	modeConfig = config.sheet_by_name('mode')
	functionConfig = config.sheet_by_name('function')

	status = modeConfig.cell(0,1).value
	mode = modeConfig.cell(1,1).value
	signal = modeConfig.cell(2,1).value	# 读取后缀符号
	root = modeConfig.cell(3,1).value
	
	readOrder()	

def readOrder():	# 读取指令
	global mvDic
	mvDic = {}
	nrows = functionConfig.nrows
	for i in range(1,nrows):
		if functionConfig.cell(i,0).value == "mv":
			mvDic[functionConfig.cell(i,1).value] = functionConfig.cell(i,2).value

	os.chdir("../../")	# 改变工作目录,为运行文件的上上一级目录

def mv():	# 无论是文件还是目录都移动
	for file in os.listdir():
		filename = os.path.splitext(file)[0]	# 文件名
		suffix = filename.split(signal)[-1]
		dirname = mvDic.get(suffix, 0)
		if dirname != 0:
			if not os.path.exists(dirname):	# 判断是否有文件夹，没有则创建
				os.mkdir(dirname)
			shutil.move(file, dirname)

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
			dirname = mvDic.get(suffix, 0)
			if dirname != 0:
				if not os.path.exists(dirname):	# 判断是否有文件夹，没有则创建
					os.mkdir(dirname)
				shutil.move(file, dirname)	#递归地将一个文件或目录 (src) 移至另一位置 (dst) 并返回目标位置

if __name__ == '__main__':
	readConfig()
	mv()