import hashlib
import os
import time

import xlrd
import xlwt
from django.conf import settings

from apps.vadmin.system.models import SaveFile
from apps.vadmin.system.serializers import SaveFileSerializer


def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


def export_excel(field_data: list, data: list, FileName: str, file_path: str = settings.MEDIA_ROOT):
    wbk = xlwt.Workbook(encoding='utf-8')
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    style = xlwt.XFStyle()
    wbk.set_colour_RGB(0x23, 0, 60, 139)
    xlwt.add_palette_colour("custom_colour_35", 0x23)
    tab_al = xlwt.Alignment()
    tab_al.horz = 0x02
    tab_al.vert = 0x01
    tab_pattern = xlwt.Pattern()
    tab_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    tab_pattern.pattern_fore_colour = 55
    tab_fnt = xlwt.Font()
    tab_fnt.height = 200
    default_width = 14
    tab_fnt.name = u'File'
    tab_fnt.colour_index = 1
    tab_borders = xlwt.Borders()
    tab_borders.left = xlwt.Borders.THIN
    tab_borders.right = xlwt.Borders.THIN
    tab_borders.top = xlwt.Borders.THIN
    tab_borders.bottom = xlwt.Borders.THIN
    tab_borders.left_colour = 23
    tab_borders.right_colour = 23
    tab_borders.bottom_colour = 23
    tab_borders.top_colour = 23

    style.alignment = tab_al
    style.pattern = tab_pattern
    style.font = tab_fnt
    style.borders = tab_borders
    for index, ele in enumerate(field_data):
        sheet.write_merge(0, 0, index, index, ele, style)

    col_width = []
    for index, ele in enumerate(data):
        for inx, values in enumerate(ele.values()):
            if index == 0:
                col_width.append(len_byte(str(values)))
            else:
                if col_width[inx] < len_byte(str(values)):
                    col_width[inx] = len_byte(str(values))
    for i in range(len(col_width)):
        if col_width[i] > 10:
            width = col_width[i] if col_width[i] < 36 else 36
            sheet.col(i).width = 256 * (width + 6)
        else:
            sheet.col(i).width = 256 * (default_width)

    row = 1
    left_pattern = xlwt.Pattern()
    left_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    left_pattern.pattern_fore_colour = 1

    left_fnt = xlwt.Font()
    left_fnt.height = 200
    left_fnt.name = u'File'
    left_fnt.colour_index = 0

    left_style = style
    left_style.pattern = left_pattern
    left_style.font = left_fnt

    for results in data:
        for index, values in enumerate(results.values()):
            sheet.write(row, index, label=values, style=left_style)
        row += 1

    monthTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    pathRoot = os.path.join(file_path, 'system', monthTime)
    if not os.path.exists(pathRoot):
        os.makedirs(pathRoot)
    path_name = os.path.join(pathRoot, FileName)
    wbk.save(path_name)
    return os.path.join('system', monthTime, FileName)


def export_excel_save_model(request, field_data, data, FilName):
    time_stamp = hashlib.md5(str(field_data).encode('utf8')).hexdigest()
    FilName = '.'.join(FilName.split('.')[:-1]) + str(time_stamp) + '.' + FilName.split('.')[-1]
    file_rul = export_excel(field_data=field_data, data=data, FileName=FilName)
    savefile, _ = SaveFile.objects.get_or_create(file=file_rul)
    if _ == True:
        savefile.name = FilName
        savefile.type = 'application/vnd.ms-excel'
        savefile.size = os.path.getsize(os.path.join(settings.MEDIA_ROOT, file_rul))
        savefile.address = 'Lu tru cuc bo'
        savefile.source = 'Xuat'
        savefile.creator = request.user
        savefile.dept_belong_id = getattr(request.user, 'dept_id', None)
    savefile.modifier = request.user.username
    savefile.save()
    return SaveFileSerializer(savefile).data


def excel_to_data(file_url, field_data):
    data = xlrd.open_workbook(os.path.join(settings.BASE_DIR.replace('\\', os.sep), *file_url.split(os.sep)))
    table = data.sheets()[0]
    tables = []
    for i, rown in enumerate(range(table.nrows)):
        if i == 0: continue
        array = {}
        for index, ele in enumerate(field_data.keys()):
            cell_value = table.cell_value(rown, index)
            if type(cell_value) is float and str(cell_value).split('.')[1] == '0':
                cell_value = int(str(cell_value).split('.')[0])
            if type(cell_value) is str:
                cell_value = cell_value.strip(' \t\n\r')
            array[ele] = cell_value

        tables.append(array)
    return tables
