#encoding=utf-8
#python3.5
#Author: fangjun
#date: 2018-03-24

import xlrd
import xlwt

class FindExcelData(object):
    """
    按字段查找excel中的数据,
    可以按给定的字段进行全表查询,
    不仅仅可以查找资产表，可以支持查找任意标准的excel文件
    eg:
    excel = FindExcelData(input_excel, info_list, field, output_excel)
    excel.write_excel()
    excel.no_found()
    """

    def __init__(self, input_excel, info_list, field, output_excel):
        self.input_excel = input_excel
        self.info_list = info_list
        self.field = field
        self.output_excel = output_excel


    def get_sheets(self):
        try:
            wb = xlrd.open_workbook(self.input_excel)
        except:
            print('excel文件格式不正确!')
        else:
            tables = wb.sheet_names()
            return dict(zip(tables, tables))


    def get_data(self):
        data = {}
        Sheets = self.get_sheets()  # 在类内部调用类方法
        try:
            wb = xlrd.open_workbook(self.input_excel)
        except:
            pass
        else:
            for k, v in Sheets.items():
                headers, assets_list = [], []
                table = wb.sheet_by_name(v)
                nrows = table.nrows  #行数
                ncols = table.ncols  #列数

                # 获取表头,第一行数据
                headers = table.row_values(0)

                # 获取表格中的所有数据(记录),一个表格的记录保存到一个assets_list中
                for i in range(1, nrows):
                    assets_list.append( dict( zip(headers, table.row_values(i)) ) )
                data[k] = {'assets_list': assets_list, 'headers': headers}

        return data


    def filter_assets(self):
        filter_data = {}
        data = self.get_data()   # 在类内部调用类方法
        for k, v in data.items():
            assets_list = v['assets_list']
            # sheet_data = {'assets_list': []}
            tmp_data = []
            for asset in assets_list:
                for info in self.info_list:
                    if asset.get(self.field) == info:
                        tmp_data.append(asset)
                        filter_data[k] = { 'headers': v['headers'],'assets_list': tmp_data }
        return filter_data


    def write_excel(self):
        wb = xlwt.Workbook(encoding='utf-8')         # 创建一个excel工作薄
        head_style = xlwt.easyxf('font: bold on')
        filter_data = self.filter_assets()      # 在类内部调用类方法
        Sheets = self.get_sheets()

        for k,v in filter_data.items():
            sheet_name = Sheets.get(k)
            ws = wb.add_sheet(sheet_name)    # 在excel工作薄中新建一个sheet
            headers = v['headers']
            assets_list = v['assets_list']
            ncols = len(headers)            # 列数
            for i in range(ncols):          # 写入表头
                ws.write(0, i, headers[i], head_style)  # 写入第0行，第i列数据  
            
            index = 1
            for each in assets_list:       # 写入数据
                for j in range(ncols):
                    ws.write(index, j, each.get(headers[j]))  # 第index行,第j列写数据
                index += 1
        try:
            wb.save(self.output_excel)
        except:
            print('excel文件写入失败!')
        else:
            print('excel文件写入成功!')


    def no_found(self):
        filter_data = self.filter_assets()    # 在类内部调用类方法
        no_found,found = [], []
        for k, v in filter_data.items():
            assets_list = v['assets_list']
            for item in assets_list:
                found.append(item.get(self.field))
        
        #差集（把list_1里面有的而list_2里面没有的取出来）：
        # print(list_1.difference(list_2))
        try:
            self.no_found = ( set(self.info_list).difference(set(found)) )
        except NameError as e:
            pass
        return list(self.no_found)


# def get_msg(file_name):
#     info_list = []
#     with open(file_name, encoding='UTF-8') as f:
#         info_list = [ line.strip() for line in f ]
#     return info_list


if __name__ == '__main__':
    field = u'业务归属科室'
    input_excel = u'资产导出全表20180205.xls'
    file_name = 'ip.txt'
    # info_list = get_msg('ip.txt')
    info_list = []
    output_excel = 'output.xls'

    excel = FindExcelData(input_excel, info_list, field, output_excel)
    excel.write_excel()

    print( 'no found....\n', excel.no_found() )
    print( '************************end************************' )