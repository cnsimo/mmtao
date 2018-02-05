#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-02 23:11:08
# @Author  : cnsimo (2020745751@qq.com)
# @Link    : http://www.scriptboy.com
# @Version : 1.0

from myheaders import getUA
import requests
import re
import time
import csv

mmListUrl = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
mmUrl = ''

# 获得总共的页数
def getTotalPage():
	headers = {'User-Agent': getUA()}
	req = requests.get(mmListUrl, headers=headers)
	res = req.json()
	return res['data']['totalPage']

# 获取列表的函数
def getMMList(cpage = 1):
	headers = {'User-Agent': getUA()}
	payload = {'currentPage': cpage, 'pageSize': 100, 'sortType': 'default', 'viewFlag': 'A'}
	req = requests.post(mmListUrl, headers=headers, data=payload)
	res = req.json()
	if 'data' in res.keys():
		return res['data']['searchDOList']
	else:
		return

if __name__ == '__main__':
	totalPage = getTotalPage()
	with open(r'mmlist.csv', 'w+', newline='') as fs:
		count = 1
		cpage = 1
		csvwriter = csv.writer(fs, dialect='excel')
		page1 = getMMList(cpage)
		csvwriter.writerow(page1[0].keys())
		print('正在处理第%s页。。。' % cpage)
		for mm in page1:
			csvwriter.writerow(mm.values())
			print(str(count)+' ', end='')
			count += 1
		print()
		while cpage < totalPage:
			cpage += 1
			print('正在处理第%s页。。。' % cpage)
			time.sleep(2)
			mmList = getMMList(cpage)
			if not mmList:
				break
			for mm in mmList:
				csvwriter.writerow(mm.values())
				print(str(count)+' ', end='')
				count += 1
			print('')

	print('所有数据处理完毕!')
