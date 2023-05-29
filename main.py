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
    else:
        domesticType="N"
    print('domesticType:',domesticType,'brandName:',elemBrand['name'])
    response = requests.get(
        'https://api.encar.com/search/car/list/mobile?count=true&q=(And.Hidden.N._.(C.CarType.{}._.Manufacturer.{}.))&inav=%7CMetadata%7CSort'.format(domesticType,elemBrand['name']),
        headers=headers,
    )

    result=json.loads(response.text)
    # pprint.pprint(result)
    with open('output.json', 'w',encoding='utf-8-sig') as f:
        json.dump(result, f, indent=2,ensure_ascii=False)


    result1 = result['iNav']['Nodes'][1]['Facets'][elemBrand['brandIndex']]['Refinements']["Nodes"][0]['Facets'][elemBrand['countIndex']]['Refinements']['Nodes'][0]['Facets']
    # result1=result['iNav']['Nodes'][1]['Facets'][1]['Refinements']["Nodes"][0]['Facets'][elemBrand['countIndex']]['Refinements']['Nodes'][0]['Facets']


    with open('output.json', 'w',encoding='utf-8-sig') as f:
        json.dump(result1, f, indent=2,ensure_ascii=False)


    for elem1 in result1:
        name=elem1['DisplayValue']
        print(name)



totalBrand=getDomesticBrand()
print('totalBrand:',totalBrand)
print("===============")
for elemBrand in totalBrand:
    getDetail(elemBrand)
    time.sleep(random.randint(5,10)*0.1)
