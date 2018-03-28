#encoding=utf-8
#python3.5
#date: 2018-03-23
#function:按字段查找,V5版本，可以按给定的字段在excel中全表查询

import xlrd
import xlwt

def get_sheets(excelFile):
    wb = xlrd.open_workbook(excelFile)
    tables = wb.sheet_names()
    return dict( zip(tables, tables) )


def get_data(excelFile, Sheets):
    data = {}
    wb = xlrd.open_workbook(excelFile)
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


def filter_assets(data, info_list, field):
    filter_data = {}
    
    for k, v in data.items():
        assets_list = v['assets_list']
        sheet_data = {'assets_list': []}
        for asset in assets_list:
            for info in  info_list:
                if asset.get(field) == info:
                    sheet_data['assets_list'].append(asset)
                    filter_data[k] = { 'headers': v['headers'],'assets_list': sheet_data.get('assets_list') }
    return filter_data


def write_excel(filter_data, Sheets, output='output.xls'):
    wb = xlwt.Workbook(encoding='utf-8')         # 创建一个excel工作薄
    head_style = xlwt.easyxf('font: bold on')
    
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
        wb.save(output)
    except:
        print('文件写入失败!')
    else:
        print('文件写入成功!')


def get_msg(file_name):
    info_list = []
    with open(file_name, encoding='utf-8') as f:
        info_list = [ line.strip() for line in f ]
    return info_list


def no_found(field, info_list, filter_data):
    no_found,found = [], []
    for k, v in filter_data.items():
        assets_list = v['assets_list']
        for item in assets_list:
            found.append(item.get(field))
    

    no_found = (set(info_list).difference(set(found)) )
    return list(no_found)


if __name__ == '__main__':
    field = u'名称'
    info_list = get_msg('ip.txt')
    file_name = 'ip.txt'
    excelFile = u'test.xlsx'

    Sheets = get_sheets(excelFile)
    data = get_data(excelFile, Sheets)
    filter_data = filter_assets(data, info_list, field)
    write_excel(filter_data, Sheets)
    no_found = no_found(field, info_list, filter_data)

    print('no found....\n',no_found)