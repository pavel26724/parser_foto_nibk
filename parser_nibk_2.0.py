import requests
import os
import openpyxl
import time
from bs4 import BeautifulSoup

_BSDIR = os.path.dirname(os.path.abspath(__file__))

def parser_nibk_foto():
    base = openpyxl.open(os.path.join(_BSDIR, 'price_ads.xlsx'))
    sheet_base = base.active
    book_rez = openpyxl.Workbook()
    sheet_rez = book_rez.active
    x = []
    for s in sheet_base.iter_rows(max_row=None):
        x.append(s[0].value)

    sheet_rez.append(['Артикул', 'Ссылка на фото без ВЗ', 'Ссылка на фото с ВЗ'])
    o = []
    for x1 in x:
        response = requests.post(
            url = 'https://jnbk-brakes.com/catalogue/cars',
            data={"txtPartNo": x1, "txtClass": 1, "btnProductSearch": "Search"},
        )

        soup = BeautifulSoup(response.text, 'lxml')
        picture_d = soup.find('div', class_='detail__gallery')
        try:
            picture_url = picture_d.find('img').get('src')   #без водяных знаков
            picture_url_watermark = picture_d.find('a').get('href')   #с водяными знаками
        except AttributeError:
            picture_url = 'no foto'
            picture_url_watermark = 'no foto'

        sheet_rez.append([x1, picture_url, picture_url_watermark])
        print(f'Артикул: {x1}, ссылка без ВЗ: {picture_url}, ссылка с ВЗ: {picture_url_watermark}')

    book_rez.save(f'parser_nibk_foto.xlsx')
    book_rez.close()

start_time = time.time()
parser_nibk_foto()
print(f'отработала за {int(time.time() - start_time)} секунд = {round((int(time.time() - start_time))/60, 2)} минут')