# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta  # 时间相关库
import json
import urllib.request
import urllib.parse
import ssl
import os

version = 'v3'  # v3版本:数据更新日期2021.5   v2版本：数据更新日期2020.4
base_url = "https://geo.datav.aliyun.com/areas_"+version+"/bound/"  # 基本请求地址
backup_url = "https://geo.datav.aliyun.com/areas_v2/bound/"
# 获取


def getAreaCodeType(code):
    if code[2:6] == "0000":
        return "1"
    elif code[4:6] == "00":
        return "2"
    else:
        return "3"

# 请求失败重试


def retry(times):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            i = 0
            while i < times:
                try:
                    if i > 0:

                        if i == 3:
                            if args[1] == 'infos.json':
                                print('尝试第1次切换为v2版本地址:%s%s' %
                                      (args[2], args[1]))
                                back = args[2]
                                return func(back, args[1], args[2])
                            else:
                                print('尝试切换为不包含子域的接口地址（v3版本问题）')
                                return func(args[0], args[1], ".json", args[3], args[4])

                                # print('尝试切换为v2版本地址:%s%s%s' %
                                #       (args[3], args[1], args[2]))
                                # back = args[3]
                                # return func(back, args[1], args[2], args[3], args[4])
                        if i == 4:
                            if args[1] == 'infos.json':
                                print('尝试第2次切换为v2版本地址:%s%s' %
                                      (args[2], args[1]))
                                back = args[2]
                                return func(back, args[1], args[2])
                            else:
                                print('尝试切换为v2版本地址:%s%s%s' %
                                      (args[3], args[1], args[2]))
                                back = args[3]
                                return func(back, args[1], args[2], args[3], args[4])

                        print('正在尝试第%d次请求' % (i+1))

                    return func(*args, **kwargs)
                except urllib.request.URLError as e:
                    if args[1] == 'infos.json':
                        print('%s%s 请求失败!' % (args[0], args[1]))
                        WriteToErrorFile(e, args[0]+''+args[1])
                    else:
                        print('%s%s%s 请求失败!' % (args[0], args[1], args[2]))
                        WriteToErrorFile(e, args[0]+''+args[1]+''+args[2])
                    i += 1
        return inner_wrapper
    return wrapper


def WriteDataToFile(url, data):
    try:
        with open(url, "xt", encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False)
            print("写入", url)
    except FileExistsError as e:
        print('文件已存在，跳过'+str(e))


def WriteToErrorFile(e, url):
    with open('Error.txt', "a+", encoding='utf-8') as e_file:
        e_file.writelines(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")+'\n'+str(e)+'\nin request:'+url+'\n\n')


def isExsists(*args):
    if os.path.exists(args[5]):
        print("文件已存在，跳过[Errno 17] File exists: '", args[5]+"'")
    else:
        args[0](*args[1:])


@retry(5)
def fetchCountyData(u, item, suffix, backup_url, path):
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(
        u + item + suffix,
        context=context,
        timeout=5
    ) as res:
        print(
            "请求：" + u + item + suffix
        )
        text = json.loads(res.read().decode("UTF-8"))
        WriteDataToFile(path, text)


@retry(5)
def fecthFullData(u, item, suffix, backup_url, path):
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(
        u + item + suffix,
        context=context,
        timeout=5
    ) as res:
        print(
            "请求："+u
            + item
            + suffix
        )
        text = json.loads(res.read().decode("UTF-8"))
    WriteDataToFile(path, text)
    # if item == "100000":
    #     WriteDataToFile("china.json", text, item)
    # elif getAreaCodeType(item) == "1":
    #     WriteDataToFile("province/" + item +
    #                     ".json", text, item)
    # elif getAreaCodeType(item) == "2":
    #     WriteDataToFile("citys/" + item +
    #                     ".json", text, item)


@retry(5)
def fetchData(u, addr, backup_url):
    context = ssl._create_unverified_context()
    url = u+addr
    with urllib.request.urlopen(url, context=context, timeout=5) as response:
        print("请求接口并写入文件中。。。")
        html = json.loads(response.read().decode("UTF-8"))
        WriteDataToFile("location.json", html)
        for item in list(html.keys()):
            if getAreaCodeType(item) == "3":
                path = "county/" + item + '.json'
                isExsists(fetchCountyData, base_url,
                          item, '.json', backup_url, path)
                # with urllib.request.urlopen(
                #     base_url + item + ".json",
                #     context=context,
                #     timeout=5
                # ) as res:
                #     print(
                #         "请求：" + base_url + item + ".json"
                #     )
                #     text = json.loads(res.read().decode("UTF-8"))
                #     WriteDataToFile("county/" + item +
                #                     ".json", text, item)
            else:
                path = ''
                if item == "100000":
                    path = "china.json"
                elif getAreaCodeType(item) == "1":
                    path = "province/" + item + ".json"
                elif getAreaCodeType(item) == "2":
                    path = "citys/" + item + ".json"
                isExsists(fecthFullData, base_url, item,
                          "_full.json", backup_url, path)
                # fecthFullData(base_url, item, "_full.json", backup_url)
                # with urllib.request.urlopen(
                #     base_url + item + "_full.json",
                #     context=context,
                #     timeout=5
                # ) as res:
                #     print(
                #         "请求："+base_url
                #         + item
                #         + "_full.json"
                #     )
                #     text = json.loads(res.read().decode("UTF-8"))
                # if item == "100000":
                #     WriteDataToFile("china.json", text, item)
                # elif getAreaCodeType(item) == "1":
                #     WriteDataToFile("province/" + item +
                #                     ".json", text, item)
                # elif getAreaCodeType(item) == "2":
                #     WriteDataToFile("citys/" + item +
                #                     ".json", text, item)
    # except urllib.request.URLError as e:
    #     print("请求出现异常: "+str(e))
    #     WriteToErrorFile(e, url)


if not os.path.isdir("province"):
    os.mkdir("province")
    print("创建province文件夹")
if not os.path.isdir("citys"):
    os.mkdir("citys")
    print("创建citys文件夹")
if not os.path.isdir("county"):
    os.mkdir("county")
    print("创建county文件夹")
fetchData(base_url, 'infos.json', backup_url)
