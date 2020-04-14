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
if not os.path.isdir("citys"):
    os.mkdir("citys")
if not os.path.isdir("county"):
    os.mkdir("county")
context = ssl._create_unverified_context()
url = "https://geo.datav.aliyun.com/areas_v2/bound/infos.json"
with urllib.request.urlopen(url, context=context) as response:
    html = json.loads(response.read().decode("utf-8"))
    with open("location.json", "w") as json_file:
        json.dump(html, json_file)
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
                text = json.loads(res.read().decode("utf-8"))
                with open("county/" + item + ".json", "w") as json_file:
                    json.dump(text, json_file)
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
                text = json.loads(res.read().decode("utf-8"))
            if item == "100000":
                with open("china.json", "w") as json_file:
                    json.dump(text, json_file)
                    print("写入", item)
            elif getAreaCodeType(item) == "1":
                with open("province/" + item + ".json", "w") as json_file:
                    json.dump(text, json_file)
                    print("写入", item)
            elif getAreaCodeType(item) == "2":
                with open("citys/" + item + ".json", "w") as json_file:
                    json.dump(text, json_file)
                    print("写入", item)
