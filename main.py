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
        'local_big_cover': kwargs['local_big_cover'],
        'create_time': datetime.datetime.now()
    }
    return jav


def get_jav_collection():
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['test']
    return db['javs']


def start_download_img(url, path):
    t = DownloadThread(arg=(url, path))
    t.setDaemon(True)
    t.start()


def cleanup():
    coll = get_jav_collection();
    coll.remove()
    if os.path.exists('covers'):
        shutil.rmtree('covers')


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
            local_small_cover = 'covers/' + number + '_small.jpg'
            start_download_img(url=small_cover_url, path=local_small_cover)

            details_url = item.find('.movie-box').attr("href")
            container = spider.getdoc(url=details_url)('.container')

            big_cover_url = container.find('.bigImage img').attr('src')
            local_big_cover = 'covers/' + number + '.jpg'
            start_download_img(url=big_cover_url, path='covers/' + number + '.jpg')

            movie_info = container.find('.info')

            jav = get_jav(number=number, details_url=details_url, small_cover_url=small_cover_url,
                          local_small_cover=local_small_cover, big_cover_url=big_cover_url,
                          local_big_cover=local_big_cover)
            print(jav)
            collection.insert_one(jav)
            # print(movie_info)
            # print(container.find('#sample-waterfall'))
