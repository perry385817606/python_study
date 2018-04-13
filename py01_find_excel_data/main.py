#encoding=utf-8
import sys
import datetime
import gconf
from utils import find_excel as find
from utils.file_oper_read import FileRead
from utils.file_oper_write import FileWrite

# 为了避免文件读写类和excel操作类模块间循环引用的问题,暂时将文件写操作拆分成一个独立的模块
if __name__ == '__main__':
    starttime = datetime.datetime.now()
    
    # 实例化一个读文件的对象
    readFile = FileRead(gconf.file_name)

    # 调用read_file()方法
    info_list = readFile.read_file()

    # 实例化excel对象
    excel = find.FindExcelData( gconf.excelFile, 
                                info_list, 
                                gconf.field, 
                                gconf.output_excel,
                               )
    excel.write_excel()
    no_found = excel.no_found()
    print(no_found)
    # 实例化一个写文件的对象
    writeFile = FileWrite(gconf.output, no_found)

    # 调用excel写方法
    writeFile.write_file()
    
    print(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    endtime = datetime.datetime.now()
    print( '************************end************************' )
    print( '程序运行了%s秒' %(endtime - starttime).seconds )
