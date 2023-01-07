import requests
import os
import openpyxl
import time

_BSDIR = os.path.dirname(os.path.abspath(__file__))

def parser_nibk_foto():
    base = openpyxl.open(os.path.join(_BSDIR, 'price_ads.xlsx'))
    sheet_base = base.active
    book_rez = openpyxl.Workbook()
    sheet_rez = book_rez.active
    x = []
    for s in sheet_base.iter_rows(max_row=None):
        x.append(s[0].value)

    sheet_rez.append(['Артикул', 'Ссылка на фото'])
    o = []
    for x1 in x:
        response = requests.post(
            url = 'https://jnbk-brakes.com/catalogue/cars',
            data={"txtPartNo": x1, "txtClass": 1, "btnProductSearch": "Search"},
        )

        with open('rez_file.txt', 'wb') as f:
            f.write(response.content)

        file = open("rez_file.txt", 'r', encoding="utf-8")
        for line in file:
            if 'achrColorBox' in line:
                url_rez = line.split()[2].replace('href="', '').replace('"', '')
                sheet_rez.append([x1, url_rez])
                # print(f'Артикул: {x1}, ссылка: {url_rez}')

    book_rez.save(f'parser_nibk_foto.xlsx')
    book_rez.close()

start_time = time.time()
parser_nibk_foto()
print(f'отработала за {int(time.time() - start_time)} секунд = {(int(time.time() - start_time))/60}минут')