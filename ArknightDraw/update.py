# -*- encoding:utf-8 -*-
import asyncio
import os
from urllib.parse import unquote
import re

import aiofiles as aiofiles
import aiohttp
from lxml import etree, html


class TableData:
    pass


class CharData:
    name: str  # 名称
    star: int  # 星级
    limited: bool  # 限定
    getWay: str  # 获得途径
    pass


class UpdateHandle:

    def __init__(self, data_path: str, conf_path: str):
        self.headers = {
            "User-Agent": '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'
        }
        self.data_path = data_path
        self.conf_path = conf_path
        pass

    def get_char_data(self):
        pass

    def get_table_data(self):
        pass

    def get_up_table(self):
        pass

    async def download_file(self, url: str, name: str, path: str) -> bool:
        r"""下载文件

        :param url: 指定发送群号
        :param name: 文件名
        :param path: 储存目录
        :rtype bool
        """
        dir_path = self.data_path + path
        file_path = self.data_path + path + name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            return True
        if os.path.exists(file_path):
            return True
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=10) as response:
                    async with aiofiles.open(str(file_path), "wb") as f:
                        await f.write(await response.read())
            print(f"下载文件{name}成功，url：{url}，储存目录：{path}")
            return True
        except TimeoutError:
            print(f"下载文件{name} 超时，url：{url}")
            return False
        except:
            print(f"下载文件 {name} 链接错误，url：{url}")
            return False

    def request_data(self, url: str, cookie: list):
        pass


    async def get_url(self, url: str) -> str:
        result = ""
        retry = 5
        for i in range(retry):

            try:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url) as resp:
                        result = await resp.text()
                break
            except TimeoutError:
                self.log_print()
                await asyncio.sleep(1)
        return result

    def log_print(self, message: str) -> bool:
        pass

    def test(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.get_info())


if __name__ == "__main__":
    app = UpdateHandle("../data/", "../conf/")
    app.test()
