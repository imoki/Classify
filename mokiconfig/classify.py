# 将文件自动分类

import os
import xlrd
import xlwt
import shutil

def readConfig():	# 读取配置文件
	global config, modeConfig, functionConfig, status, mode, signal, root
	config = xlrd.open_workbook(r'./config.xls')
	modeConfig = config.sheet_by_name('mode')
	functionConfig = config.sheet_by_name('function')

	status = modeConfig.cell(0,1).value
	mode = modeConfig.cell(1,1).value
	signal = modeConfig.cell(2,1).value
	root = modeConfig.cell(3,1).value

def mvFile():	# 移动文件
	mvDic = {}
	nrows = functionConfig.nrows
	for i in range(1,nrows):
		if functionConfig.cell(i,0).value == "mv":
			mvDic[functionConfig.cell(i,1).value] = functionConfig.cell(i,2).value

	os.chdir("../")	# 改变工作目录
	for file in os.listdir():
		if(os.path.isfile(file)):	# 是文件
			filename = os.path.splitext(file)[0]	# 文件名
			suffix = filename.split(signal)[-1]
			dirname = mvDic[suffix]
			if not os.path.exists(dirname):	# 判断是否有文件夹，没有则创建
				os.mkdir(dirname)
			shutil.move(file, dirname)

if __name__ == '__main__':
	readConfig()
	mvFile()