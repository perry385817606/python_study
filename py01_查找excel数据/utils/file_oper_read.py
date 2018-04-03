#encoding=utf-8
import sys
sys.path.append('../')
# print(sys.path)
import gconf

class FileRead():
	'''
	文件读写,读入待查找的数据
	read_file()方法返回一个list;
	'''
	def __init__(self, input_file):
		self.input_file = input_file


	def read_file(self):
	    info_list = []
	    try:
	    	with open(self.input_file, encoding='UTF-8') as f:
	    		info_list = [ line.strip() for line in f ]
	    except UnicodeDecodeError as e:
	    	print(e,'\n','Unicode 解码时的错误, txt文件格式不对,请将文件修改为UTF-8编码的格式!')
	    	# return info_list
	    else:
	    	return list(set(info_list))   # 去掉ip.txt中重复的数据


# data = ['10.211.152.254', '100.100.100.100']
# data = ['\ufeff', '10.211.152.254', '100.100.100.100']   # ?
if __name__ == '__main__':
	print(gconf.file_name)
	File = FileRead(gconf.file_name)
	print(File.read_file())
	
