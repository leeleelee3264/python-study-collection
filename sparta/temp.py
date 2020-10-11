# python to excel test code
from openpyxl import Workbook

wb = Workbook()
ws1 = wb.active
ws1.title = "articles"
ws1.append(["제목", "링크", "신문사"])
ws1.append(['1', '2', '3'])
wb.save(filename='articles.xlsx')