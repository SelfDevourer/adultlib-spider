import datetime
import os
import shutil

import pymongo

from DownloadThread import DownloadThread
from Spider import Spider


def get_jav(**kwargs):
    jav = {
        'number': kwargs['number'],
        'details_url': kwargs['details_url'],
        'small_cover': kwargs['small_cover_url'],
        'local_small_cover': kwargs['local_small_cover'],
        'big_cover': kwargs['big_cover_url'],
        'local_big_cover': kwargs['local_big_cover'], 'title': kwargs['title'],
        'create_time': datetime.datetime.now()
    }
    jav.update(kwargs['info'])
    return jav


def get_jav_collection():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['test']
    return db['javs']


def start_download_img(url, file_name):
    t = DownloadThread(arg=(url, file_name))
    t.setDaemon(True)
    t.start()


def cleanup():
    coll = get_jav_collection();
    coll.remove()
    folder_path = 'E:/workspace/adultlib/src/main/resources/static/covers/'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def get_text(key, info):
    text = info('span.header:contains(' + key + ')').parent().text()
    return text.split(' ')[1] if text != '' else None


collection = get_jav_collection()
# cleanup()

spider = Spider(basic_url='#')
page_count = spider.get_page_count()
print('The page count %d' % page_count)
for i in range(1, page_count):
    items = spider.getdoc(path="page/" + str(i))('.item').items()
    print("Visiting in page %d" % i)
    for item in items:
        number = item.find('.photo-info date:first').text()
        result = collection.find_one({'number': number})
        if result is None:
            small_cover_url = item.find('img').attr("src")
            start_download_img(url=small_cover_url, file_name=number + '_small')

            details_url = item.find('.movie-box').attr("href")
            container = spider.getdoc(url=details_url)('.container')

            big_cover_url = container.find('.bigImage img').attr('src')
            start_download_img(url=big_cover_url, file_name=number)

            title = container('h3').text()
            title = title[len(number) + 1:len(title)]

            movie_info = container.find('.info')
            info_dict = {
                'release_date': get_text(key='發行日期', info=movie_info),
                'movie_len': get_text(key='長度', info=movie_info),
                'director': get_text(key='導演', info=movie_info),
                'maker': get_text(key='製作商', info=movie_info),
                'publisher': get_text(key='發行商', info=movie_info),
                'series': get_text(key='系列', info=movie_info)
            }

            jav = get_jav(number=number, details_url=details_url, small_cover_url=small_cover_url,
                          local_small_cover='/covers/' + number + '_small.jpg', big_cover_url=big_cover_url,
                          local_big_cover='/covers/' + number + '.jpg', title=title, info=info_dict)
            print(jav)
            collection.insert_one(jav)
            # print(movie_info)
            # print(container.find('#sample-waterfall'))
