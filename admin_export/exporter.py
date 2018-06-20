from io import BytesIO

import xlwt
from django.http import HttpResponse
from django.utils import timezone


# parent class of exporters
class BaseExporter:
    def __init__(self, file_name, headers, datas):
        self.file_name = file_name
        self.headers = headers
        self.datas = datas

    def filename_with_timestamp(self):
        return '{}_{}'.format(self.file_name, timezone.now().strftime('%Y%m%d%H%M%S'))

    def export(self):
        pass


# excel file exporter
class XlsExporter(BaseExporter):
    def export(self):
        workbook = xlwt.Workbook(encoding='utf8')
        sheet = workbook.add_sheet('Results')
        for i, col in enumerate(self.headers):
            sheet.write(0, i, col)

        for i, row in enumerate(self.datas):
            for j, val in enumerate(row):
                sheet.write(i + 1, j, val)

        excel = BytesIO()
        workbook.save(excel)
        excel.seek(0)

        file_name = self.filename_with_timestamp()
        response = HttpResponse(excel.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(file_name)
        return response


# xml file exporter
class XmlExporter(BaseExporter):
    pass


def getExporter(file_type):
    if file_type == 'xls':
        return XlsExporter
    elif file_type == 'xml':
        return XmlExporter
    else:
        raise AssertionError('invalid file type : {}'.format(file_type))
