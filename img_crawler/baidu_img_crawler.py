# Not currently working, please use "img_crawler/icr.py"

import os
import re
import sys
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error

from random import randint
import time
import tqdm
import pandas as pd

timeout = 5
socket.setdefaulttimeout(timeout)

# TODO
# 1. Fix crawler, seems like it's returning a gzip file
#    instead of a webpage
# 2. Might be a timing error

class Crawler:
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    __per_page = 30

    def __init__(self, t=0.1, save_path="./"):
        self.time_sleep = t
        self.save_path = save_path


    @staticmethod
    def get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'


    def save_image(self, rsp_data, word):
        if not os.path.exists(self.save_path + word):
            os.mkdir(self.save_path + word)
        # evaluate name to detect duplicates
        self.__counter = len(os.listdir(self.save_path + word)) + 1
        try: print(rsp_data['message'])
        except Exception: pass
        for image_info in rsp_data['data']:
            try:
                if 'replaceUrl' not in image_info or len(image_info['replaceUrl']) < 1:
                    continue
                obj_url = image_info['replaceUrl'][0]['ObjUrl']
                thumb_url = image_info['thumbURL']
                url = 'https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=%s&thumburl=%s' % (
                    urllib.parse.quote(obj_url), urllib.parse.quote(thumb_url))
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(obj_url)
                # Set UA andreferrer, reduce 403
                opener = urllib.request.build_opener()
                opener.addheaders = [('Accept-Encoding', 'gzip, deflate, br'),
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'),
                ]
                urllib.request.install_opener(opener)
                # save image
                filepath = f'{self.save_path}/{word}_{str(self.__counter)+str(suffix)}'
                for _ in range(5):
                    urllib.request.urlretrieve(url, filepath)
                    if os.path.getsize(filepath) >= 5:
                        break
                if os.path.getsize(filepath) < 5:
                    print("Blank file, skipping")
                    os.unlink(filepath)
                    continue
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("Unknown error")
                continue
            else:
                print("have" + str(self.__counter) + "images")
                self.__counter += 1
        return


    def get_images(self, word):
        search = urllib.parse.quote(word)
        # pn int number of images
        pn = self.__start_amount
        print(f"Collecting {word}!")
        while pn < self.__amount:

            # url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%s&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=%s&rn=%d&gsm=1e&1594447993172=' % (
            #     search, search, str(pn), self.__per_page)
            url = f"https://image.baidu.com/search/index?tn=baiduimage&word={search}"
            
            # avoid the 403
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read()
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                # decode json
                try:
                    rsp_data = json.loads(rsp)
                    self.save_image(rsp_data, word)
                    # read the next page
                    print("Downloading next page")
                    pn += 60
                except Exception as e:
                    print(e)
                    continue
            # finally:
            #     page.close()
        print("Finished downloading")
        return


    def start(self, word, total_page=2, start_page=1, per_page=100):
        """
        entry point for the crawler
        :param word: keyword to get images of
        :param total_page: how many pages you want, total images would be total_page x per_page
        :param start_page:start page
        :param per_page: how many images per page
        :return: 
        """

        self.__per_page = per_page
        self.__start_amount = (start_page - 1) * self.__per_page
        self.__amount = total_page * self.__per_page + self.__start_amount
        self.get_images(word)


if __name__ == '__main__':

    crawler = Crawler(1, save_path=r"\imgs")

    keywords = ["摩托车", "香港摩托车", "大巴", "公共汽车", "巴士", "香港大巴", "香港公共汽车", 
                "香港巴士", "自行车", "单车", "香港自行车", "香港单车", "香港有轨电车"]

    for kw in keywords:
        crawler.start(kw)
