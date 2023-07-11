# -*- encoding:utf-8 -*-
import json
import time
from tqdm import tqdm, trange
from ArknightDraw.update import *


class UpdateHandleArk(UpdateHandle):
    def __init__(self, data_path: str, conf_path: str):
        super().__init__(data_path, conf_path)

    # 获取人物更新信息
    async def get_info(self):
        char_data_list = {}
        simple_star_list = {
            6: [],
            5: [],
            4: [],
            3: []
        }
        limit_activity = {
            "全部活动":[],
            "linkage":{},
            "limit_":{}
        }
        url = "https://wiki.biligame.com/arknights/干员数据表"
        result = await self.get_url(url)
        if not result:
            return ""
        dom = etree.HTML(result, etree.HTMLParser())
        char_list = dom.xpath("//table[@id='CardSelectTr']/tbody/tr")
        for char in trange(len(char_list), desc="处理人物素材", unit="char"):
            char = char_list[char]
            try:
                # 获取基本信息
                avatar = char.xpath("./td[1]/div/div/div/a/img/@srcset")[0]
                name = char.xpath("./td[2]/a/text()")[0]
                profession = char.xpath("./td[4]/img/@alt")[0]
                star = char.xpath("./td[5]/text()")[0]
                sources = [_.strip('\n') for _ in char.xpath("./td[8]/text()")]

                # 获取半身图/全身立绘
                url_root = "https://prts.wiki/w/文件:半身像_" + name + "_1.png"
                result = await self.get_url(url_root)
                if not result:
                    return ""
                dom = etree.HTML(result, etree.HTMLParser())
                image_url_1 = dom.xpath("//img[@decoding='async' and @width='180'and @height='360']/@src")
                image_url_path = re.search("\/\w+\/\w+\/\w+", image_url_1[0], re.M | re.I)
            except IndexError:
                continue
            char_dict = {
                "头像": unquote(str(avatar).split(" ")[-2]),
                "名称": name,
                "职业": str(profession),
                "星级": int(str(star).strip()),
                "获取途径": sources,
                "半身像": "https://prts.wiki" + str(image_url_path.group()) + "/半身像_" + name + "_1.png",
                "立绘": "https://prts.wiki" + str(image_url_path.group()) + "/立绘_" + name + "_1.png"
            }
            # print(json.dumps(char_dict, ensure_ascii=False, indent=2))

            # 稀有度分类
            if "标准寻访" in char_dict["获取途径"]:
                if char_dict["星级"] == 6:
                    simple_star_list[6].append(name)
                elif char_dict["星级"] == 5:
                    simple_star_list[5].append(name)
                elif char_dict["星级"] == 4:
                    simple_star_list[4].append(name)
                elif char_dict["星级"] == 3:
                    simple_star_list[3].append(name)

            char_data_list[name] = char_dict

        # print(json.dumps(char_data_list, ensure_ascii=False, indent=2))
        json_write(self.data_path + 'simple_star_list.json',simple_star_list)
        json_write(self.data_path + 'char_data_list.json', char_data_list)
        return char_data_list

    # 下载图片数据
    async def char_image_download(self, char_list):
        download_path = "image/char/"
        with tqdm(range(len(char_list)), desc="下载图片素材", unit="char") as pbar:
            for char in range(len(char_list)):
                name = list(char_list)[char]
                await self.download_file(char_list[name]["半身像"], "半身像_" + name + ".png", download_path)
                await self.download_file(char_list[name]["立绘"], "立绘_" + name + ".png", download_path)
                pbar.set_postfix(prograss=str(name) + "下载完毕")
                pbar.update(1)

    def start_update(self):

        loop = asyncio.get_event_loop()
        char_list = loop.run_until_complete(self.get_info())

        loop.run_until_complete(self.char_image_download(char_list))


def json_write(path, data) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    except:
        return False


def json_read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
        return json.loads(data)
    except:
        return False


if __name__ == "__main__":
    UpdateHandleArk("../data/Arknights/", "../conf/Arknights/").start_update()
