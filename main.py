import requests
import os
import bs4
import re
import json

def download(url):
    res = requests.get(url)
    bs = bs4.BeautifulSoup(res.text, features='html.parser')
    title = '%s_%s' % (re.match('.*stickershop\/product\/(\d+).*', url)[1], bs.select('.mdCMN38Item01Ttl')[0].text)
    print(title)
    if not os.path.exists(title) or os.path.isfile(title):
        os.mkdir(title)
    pic_urls = []
    for li in bs.select('.mdCMN09Li.FnStickerPreviewItem'):
        data_preview = json.loads(li.attrs['data-preview'])
        if data_preview['type'] == 'static':
            pic_url = data_preview['staticUrl']
        elif data_preview['type'] == 'animation':
            pic_url = data_preview['animationUrl']
        
        pic_url = pic_url[:pic_url.find(';')]
        print(pic_url, end='...')
        pic_res = requests.get(pic_url)
        with open(os.path.join(title, '%s_%s.png' % (data_preview['id'], data_preview['type'])), 'wb') as pic_file:
            pic_file.write(pic_res.content)
        print('done')


urls = input('urls(split with ,): ').split(',')

for url in urls :
    download(url)