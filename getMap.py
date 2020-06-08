# -*- coding: UTF-8 -*-

import json
import urllib.request
import urllib.parse
import ssl
import os


def getAreaCodeType(code):
    if code[2:6] == "0000":
        return "1"
    elif code[4:6] == "00":
        return "2"
    else:
        return "3"


if not os.path.isdir("province"):
    os.mkdir("province")
    print("创建province文件夹")
if not os.path.isdir("citys"):
    os.mkdir("citys")
    print("创建citys文件夹")
if not os.path.isdir("county"):
    os.mkdir("county")
    print("创建county文件夹")
context = ssl._create_unverified_context()
url = "https://geo.datav.aliyun.com/areas_v2/bound/infos.json"
with urllib.request.urlopen(url, context=context) as response:
    print("请求接口并写入文件中。。。")
    html = json.loads(response.read().decode("UTF-8"))
    with open("location.json", "w", encoding='utf-8') as json_file:
        json.dump(html, json_file, ensure_ascii=False)
        print("写入 location.json")
    for item in list(html.keys()):
        if getAreaCodeType(item) == "3":
            with urllib.request.urlopen(
                "https://geo.datav.aliyun.com/areas_v2/bound/" + item + ".json",
                context=context,
            ) as res:
                print(
                    "请求：https://geo.datav.aliyun.com/areas_v2/bound/" + item + ".json"
                )
                text = json.loads(res.read().decode("UTF-8"))
                with open("county/" + item + ".json", "w", encoding='utf-8') as json_file:
                    json.dump(text, json_file, ensure_ascii=False)
                    print("写入", item)
        else:
            with urllib.request.urlopen(
                "https://geo.datav.aliyun.com/areas_v2/bound/" + item + "_full.json",
                context=context,
            ) as res:
                print(
                    "请求：https://geo.datav.aliyun.com/areas_v2/bound/"
                    + item
                    + "_full.json"
                )
                text = json.loads(res.read().decode("UTF-8"))
            if item == "100000":
                with open("china.json", "w", encoding='utf-8') as json_file:
                    json.dump(text, json_file, ensure_ascii=False)
                    print("写入", item)
            elif getAreaCodeType(item) == "1":
                with open("province/" + item + ".json", "w", encoding='utf-8') as json_file:
                    json.dump(text, json_file, ensure_ascii=False)
                    print("写入", item)
            elif getAreaCodeType(item) == "2":
                with open("citys/" + item + ".json", "w", encoding='utf-8') as json_file:
                    json.dump(text, json_file, ensure_ascii=False)
                    print("写入", item)
    print("写入完成")
