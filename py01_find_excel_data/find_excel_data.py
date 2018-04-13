#python3.5
#create date: 2018-03-23
'''
说明:
v1:   2018-03-23 按给定的某一列在excel工作薄的所有sheet中查找数据, 并输出至一个新的excel文件中;
v2:   2018-03-27 增加了merge_sheet_data函数,支持sheet的合并及自定义输出列;
v3:   2018-04-13 修改main()函数,增加了自定义输出哪些sheet的功能;
v3.1: 2018-04-13 修改filter_data函数,增加了查找到记录的统计
'''
import sys
import json
import datetime
import xlrd
import xlwt
import gconf

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

    # with open('test.html','w') as f:
    #     f.write(json.dumps(data, ensure_ascii=False))
    # json_data = json.dumps(data, ensure_ascii=False)
    # print(json_data)
    return data


def filter_assets(data, info_list, field):
    filter_data = {}
    
    for k, v in data.items():
        assets_list = v['assets_list']
        # sheet_data = {'assets_list': []}
        tmp_data = []
        for asset in assets_list:
            for info in info_list:
                if asset.get(field) == info and info:    # 去掉空字符
                    # sheet_data['assets_list'].append(asset)
                    # filter_data[k] = { 'headers': v['headers'],'assets_list': sheet_data.get('assets_list') }
                    tmp_data.append(asset)
                    filter_data[k] = { 'headers': v['headers'],'assets_list': tmp_data }

    count = 0
    for v in filter_data.values():
        count += len(v['assets_list'])

    return count, filter_data


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
        print('{0} 写入失败!'.format(output))
    else:
        print('{0} 写入成功!'.format(output))


def get_msg(file_name):
    info_list = []
    try:
        with open(file_name, encoding='UTF-8') as f:
            '''
            解决了ip.txt中的字符编码问题,
            参考链接: https://blog.csdn.net/xiazhipeng1000/article/details/79720391
            https://www.cnblogs.com/mjiang2017/p/8431977.html
            '''
            info_list = [ line.encode('utf-8').decode('utf-8-sig').strip() for line in f ]
            # info_list = [ line.strip() for line in f ]
    except UnicodeDecodeError as e:
        print(e,'\n','Unicode 解码时的错误, txt文件格式不对,请将文件修改为UTF-8编码的格式!')
        # return info_list
    else:
        # print(list(set(info_list)))
        # print( type( list(set(info_list))[0] ) )
        return list(set(info_list))   # 去掉ip.txt中重复的数据


def no_found(field, info_list, filter_data):
    no_found_data,found = [], []
    for k, v in filter_data.items():
        assets_list = v['assets_list']
        for item in assets_list:
            found.append(item.get(field))
    
    no_found_data = (set(info_list).difference(set(found)))
    return list(no_found_data)


def wirte_file(info, outfile):
    if info:
        try:
            with open(outfile, 'w', encoding='utf-8') as f:
                for line in info:
                    f.write('%s\n' % str(line))
        except:
            print('%s 写入失败!' % outfile)
        else:
            print('%s 写入成功!' % outfile)
    else:
        print('没有未查找到的信息.')


def merge_sheet_data(Sheets, filter_data, outputfiled, output):
    ouput_filed = gconf.outputfiled
    fields = filter_data.values()

    count = len(fields)    # count为查找到的sheet的数量

    tmp = [ field for item in fields for field in item['headers'] ]  # 过滤出每个表的列
    headers = [ i for i in tmp if tmp.count(i) == count ]  # 找出每个表中共同的列
    headers = list(set(headers))
    # 找出不存在的列
    no_exist = [ field.strip() for field in ouput_filed  if field.strip() not in headers ] 

    if no_exist:
        print('以下列不存在于过滤的结果中:\n', no_exist)
        print()
        print('可以从以下列中选择要输出的列:\n', headers)
        return 
    else:
        headers = ouput_filed
        headers.append('所属表')
    
    # 组成一个新的assets [{'a': 1},{'a': 2},{'b': 1},{'b': 2}], old
    # 组成一个新的assets [{'a': 1,'所属表':'x86'},{'a': 2, '所属表':'刀片'},{'b': 1, '所属表':'虚拟机'}]
    megre_data, tmp = [], {}
    for k, v in filter_data.items():
        sheet_name = Sheets.get(k)
        assets = v['assets_list']
        for item in assets:
            for field in headers[0:-1:1]:
                tmp[field] = item[field]
                tmp['所属表'] = sheet_name
            megre_data.append(tmp)
            tmp = {}

        #下面两行有问题
        # tmp = dict( zip(headers[0:-1:1], [ item[field] for item in assets for field in headers[0:-1:1] ]) )
        # tmp['所属表'] = sheet_name

    wb = xlwt.Workbook(encoding='utf-8')   # 创建一个excel工作薄
    ws = wb.add_sheet('megre')    # 在excel工作薄中新建一个sheet

    head_style = xlwt.easyxf('font: bold on')
    ncols = len(headers)            # 列数
    for i in range(ncols):          # 写入表头
        ws.write(0, i, headers[i], head_style)  # 写入第0行，第i列数据

    index = 1   
    for each in megre_data:
        for j in range(ncols):
            ws.write(index, j, each.get(headers[j]))  # 第index行,第j列写数据
        index += 1
    try:
        wb.save(output)
    except:
        print('\n{0} 写入失败!'.format(output))
    else:
        print('\n{0} 写入成功!'.format(output))
 

def main():
    start_time = datetime.datetime.now()
    info_list = get_msg(gconf.file_name)

    # 选择从哪几个sheet中输出查找到的数据,当gconf.all_sheet为True时,输出查找到所有sheet的数据,
    # 当gconf.all_sheet不为True时,可以自定义输出哪些sheet的数据
    Sheets = get_sheets(gconf.input_excel)

    if gconf.all_sheet:
        Sheets = get_sheets(gconf.input_excel)
    else:
        for sheet in gconf.sheet_list:
            if sheet not in list(Sheets.keys()):
                print('{0} sheet不存在 {1}文件中,请重新选择!'.format(sheet, gconf.input_excel))
                sys.exit(2)
        Sheets = dict(zip(gconf.sheet_list, gconf.sheet_list))

    data = get_data(gconf.input_excel, Sheets)
    count, filter_data = filter_assets(data, info_list, gconf.field)
    write_excel(filter_data, Sheets)
    no_found_data = no_found(gconf.field, info_list, filter_data)
    wirte_file(no_found_data, gconf.no_found)

    # gconf.merge默认为False,不合并找到的表格
    if gconf.merge:
        merge_sheet_data(Sheets, filter_data, outputfiled = gconf.outputfiled, output = gconf.mergeoupt_excel)

    print()
    print('一共找到了%s条记录'  % count)

    end_time = datetime.datetime.now()
    print( '{0}{1}{2}'.format('*' * 40, 'end', '*' * 40) )
    print( '程序运行了%s秒' %(end_time - start_time).seconds )


if __name__ == '__main__':
    main()

