#encoding=utf-8
import sys
sys.path.append('../')
# print(sys.path)
import gconf

class FileWrite():
	'''
	文件读写,读入待查找的数据,写入没有从excel中查找到的数据
	read_file()方法返回一个list;
	write_file()方法读入一个list,输出到文件。
	'''
	def __init__(self, output_file, data=None):
		self.output_file = output_file
		self.data = data

	def write_file(self):
		if self.data:
			try:
				with open(self.output_file, 'w') as f:
			 		for line in self.data:
			 			f.write('%s\n' % str(line))
			except:
				print('txt文件写入失败!')
			else:
				print('txt文件写入成功!')
		else:
			print('没有未查找到的信息.')

# data = ['10.211.152.254', '100.100.100.100']
# data = ['\ufeff', '10.211.152.254', '100.100.100.100']   # ?
if __name__ == '__main__':
	# data = ['10.211.152.254', '100.100.100.100']
	File = FileWrite(gconf.output)
	File.write_file()

