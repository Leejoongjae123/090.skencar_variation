import json

import numpy as np

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import DataBar, FormatObject, Rule
import getmac
import requests
from bs4 import BeautifulSoup
import pprint

import requests

import requests

import requests
import time
import random
import requests

def getDomesticBrand():

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://m.encar.com',
        'Referer': 'https://m.encar.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(
        'https://api.encar.com/search/car/list/mobile?count=true&q=(And.Hidden.N._.(Or.CarType.Y._.CarType.N.))&inav=%7CMetadata%7CSort',
        headers=headers,
    )
    result=json.loads(response.text)
    # pprint.pprint(result)
    with open('output.json', 'w',encoding='utf-8-sig') as f:
        json.dump(result, f, indent=2,ensure_ascii=False)

    result1=result['iNav']['Nodes'][1]['Facets'][0]['Refinements']["Nodes"][0]['Facets']
    result2=result['iNav']['Nodes'][1]['Facets'][1]['Refinements']["Nodes"][0]['Facets']
    resultTotal=[]
    count=0
    for elem1 in result1:
        name=elem1['DisplayValue']
        data={'brandIndex':0,'countIndex':count,'name':name}
        resultTotal.append(data)
        count=count+1
    count=0
    for elem2 in result2:
        name=elem2['DisplayValue']
        data = {'brandIndex': 1, 'countIndex': count, 'name': name}
        resultTotal.append(data)
        count=count+1
    return resultTotal



def getDetail(elemBrand):
    import requests

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://m.encar.com',
        'Referer': 'https://m.encar.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    if elemBrand['brandIndex']==0:
        domesticType="Y"
        print('domesticType:', domesticType, 'brandName:', elemBrand['name'],"countIndex:",elemBrand['countIndex'])
        response = requests.get(
            'https://api.encar.com/search/car/list/mobile?count=true&q=(And.Hidden.N._.(C.CarType.{}._.Manufacturer.{}.))&inav=%7CMetadata%7CSort'.format(
                domesticType, elemBrand['name']),
            headers=headers,
        )
    else:
        domesticType="N"
        print('domesticType:', domesticType, 'brandName:', elemBrand['name'],"countIndex:",elemBrand['countIndex'])
        response = requests.get(
            'https://api.encar.com/search/car/list/mobile?count=true&q=(And.Hidden.N._.(C.CarType.{}._.Manufacturer.{}.))&inav=%7CMetadata%7CSort'.format(
                domesticType, elemBrand['name']),
            headers=headers,
        )




    result=json.loads(response.text)
    # pprint.pprint(result)
    with open('output.json', 'w',encoding='utf-8-sig') as f:
        json.dump(result, f, indent=2,ensure_ascii=False)


    if elemBrand['brandIndex']==0:
        result1 = result['iNav']['Nodes'][1]['Facets'][0]['Refinements']["Nodes"][0]['Facets'][elemBrand['countIndex']]['Refinements']['Nodes'][0]['Facets']
    else:
        result1 = result['iNav']['Nodes'][1]['Facets'][0]['Refinements']["Nodes"][0]['Facets'][elemBrand['countIndex']]['Refinements']['Nodes'][0]['Facets']



    with open('output.json', 'w',encoding='utf-8-sig') as f:
        json.dump(result1, f, indent=2,ensure_ascii=False)

    modelList=[]
    for index,elem1 in enumerate(result1):
        name=elem1['DisplayValue']
        data={'brand':elemBrand['name'],'model':name,'brandIndex':elemBrand['countIndex'],'modelIndex':index}
        print(data)
        modelList.append(data)
    print("========================")
    return modelList

def getDetailDetail(modelElem):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://m.encar.com',
        'Referer': 'https://m.encar.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    guknae=['현대','제네시스','기아','쉐보레(GM대우)','르노코리아(삼성)','KG모빌리티(쌍용)','기타 제조사']
    if modelElem['brand'] in guknae:
        domesticType="Y"
    else:
        domesticType="N"
    # print(modelElem['brand'],modelElem['model'])
    response = requests.get(
        'https://api.encar.com/search/car/list/mobile?count=true&q=(And.Hidden.N._.(C.CarType.{}._.(C.Manufacturer.{}._.ModelGroup.{}.)))&inav=%7CMetadata%7CSort'.format(domesticType, modelElem['brand'],modelElem['model']),
        headers=headers,
    )
    # print(response.text)
    result=json.loads(response.text)
    # pprint.pprint(result)
    with open('output.json', 'w',encoding='utf-8-sig') as f:
        json.dump(result, f, indent=2,ensure_ascii=False)


    # result1 = result['iNav']['Nodes'][1]['Facets'][0]['Refinements']["Nodes"][0]['Facets'][0]['Refinements']['Nodes'][0]['Facets']
    result1 = result['iNav']['Nodes'][1]['Facets'][0]['Refinements']['Nodes'][0]['Facets'][modelElem['brandIndex']]['Refinements']['Nodes'][0]["Facets"]
    with open('output2.json', 'w',encoding='utf-8-sig') as f:
        json.dump(result1, f, indent=2,ensure_ascii=False)
    print("저장완료")

    result2=result1[modelElem['modelIndex']]['Refinements']['Nodes'][0]['Facets']
    # result2 = result1[modelElem['modelIndex']]
    # pprint.pprint(result2)
    # result3=result1[46]
    # pprint.pprint(result3)

    model2List=[]
    for index,elem1 in enumerate(result2):
        name=elem1['DisplayValue']
        modelStartDate=elem1['Metadata']['ModelStartDate'][0]
        try:
            modelEndDate=elem1['Metadata']['ModelEndDate'][0]
        except:
            modelEndDate = ""
        data={'model2':name,'model2Index':index,'startDate':modelStartDate,'endDate':modelEndDate}
        modelElem.update(data)
        print('model2',name,'model2Index',index,'startDate',modelStartDate,'endDate',modelEndDate)
        print(modelElem)
        model2List.append(modelElem)


    print("========================")
    return model2List




# totalBrand=getDomesticBrand()
# print('totalBrand:',totalBrand)
# print("===============")
# totalList=[]
# for elemBrand in totalBrand:
#     modelList=getDetail(elemBrand)
#     totalList.extend(modelList)
#     time.sleep(random.randint(5,10)*0.1)
#
# with open('modelList.json', 'w') as f:
# 	json.dump(totalList, f, indent=2,ensure_ascii=False)

#↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑모델명가져오기↑↑↑↑↑↑↑↑↑↑↑↑↑

with open ('modelList.json', "r") as f:
    modelList = json.load(f)

print(modelList)
#
#
model2List=[]
exceptionList=[]
for index,modelElem in enumerate(modelList):
    if index>=2:
        break
    try:
        data=getDetailDetail(modelElem)
    except:
        print("에러로넘어감")
        exceptionList.append(modelElem)
    model2List.extend(data)
    time.sleep(random.randint(4,6)*0.1)


with open('output4.json', 'w') as f:
	json.dump(model2List, f, indent=2,ensure_ascii=False)
with open('exceptionList.json', 'w') as f:
	json.dump(exceptionList, f, indent=2,ensure_ascii=False)