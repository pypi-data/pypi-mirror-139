#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 模块重写脚本

import os
import json
from enum import Enum
from tdf_tools.tdf_print import printError

# 包含必要的数据校验
# 校验规则：配置的模块列表中必须存在且只存在一个壳应用


class REWRITE_TYPE(Enum):
    LOCAL = 1  # 本地依赖
    FEATURE = 2  # feature分支依赖
    TEST = 3  # test分支依赖


curDir = os.getcwd()

projectGenPath = curDir  # 壳工程根目录
processScriptPath = curDir + '/process/'  # 流程脚本目录
initJsonFile = 'initial_config.json'  # 流程脚本初始化信息配置json文件
moduleJsonFile = 'module_config.json'  # 流程脚本模块git相关信息json文件
# 子module的存放目录，该目录会被 gitignore 忽略
projectModuleDir = curDir + '/.project_module'


def getInitJsonData():  # 获取项目初始化数据
    os.chdir(curDir)
    with open(initJsonFile, 'r', encoding='utf-8') as readF:
        fileData = readF.read()
        readF.close()
        return json.loads(fileData)


def getModuleJsonData():  # 获取模块 git相关配置信息
    os.chdir(curDir)
    with open(moduleJsonFile, 'r', encoding='utf-8') as readF:
        fileData = readF.read()
        readF.close()
        return json.loads(fileData)


def getModuleNameList():
    initJsonData = getInitJsonData()
    if (initJsonData.__contains__('moduleNameList') and isinstance(initJsonData['moduleNameList'], list)):
        moduleNameList = initJsonData['moduleNameList']
        moduleNameList.append(initJsonData['shellName'])
        return moduleNameList
    else:
        printError("❌ 请配置moduleNameList的值,以数组形式")


def branchInvalidate():
    initJsonData = getInitJsonData()
    if (isExistKey(initJsonData, 'featureBranch') and isExistKey(initJsonData, 'testBranch') and initJsonData['featureBranch'] != '' and initJsonData['testBranch'] != '') == False:
        printError("feature和test分支必须配置，详情请参考README.md")


def moduleInvalidate():
    initJsonData = getInitJsonData()
    if initJsonData['shellName'] == "":
        printError("模块校验不通过，请确保：shellName必须配置")


def isExistKey(data, tagkey):
    key_list = data.keys()
    for key in key_list:
        if(key == tagkey):
            return True
    return False
