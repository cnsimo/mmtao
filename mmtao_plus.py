#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-03 22:07:34
# @Author  : cnsimo (2020745751@qq.com)
# @Link    : http://www.scriptboy.com
# @Version : 1.1
import re
import json
import chardet
import requests
import time
import codecs
import csv
import tqdm
from myheaders import getUA

mmListUrl = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'    # 获取模特列表的url
mmUrl = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id=' 					# 获取模特的模特卡资料的url
mmaishow = 'https://mm.taobao.com/self/aiShow.htm?userId='                              # 模特个人主页
count = 0             # 计数，你懂的
cpage = 0             # 页数，你懂的
failnum = 0            # 失败的数量


# 获得模特列表总共的页数
def getTotalPage():
	headers = {'User-Agent': getUA()}
	req = requests.get(mmListUrl, headers=headers, timeout=5)
	res = req.json()
	req.close()   # 关闭响应
	return res['data']['totalPage']

# 获取模特列表的函数
def getMMList(cpage = 1):
	headers = {'User-Agent': getUA()}
	payload = {'currentPage': cpage, 'pageSize': 100, 'sortType': 'default', 'viewFlag': 'A'}
	req = requests.post(mmListUrl, headers=headers, data=payload, timeout=5)
	res = req.json()
	req.close()  # 关闭响应
	if 'data' in res.keys():                    # 返回的数据中有可能不包含模特数据
		return res['data']['searchDOList']
	else:
		return

# 返回妹子模特卡的信息，返回一个列表
def getMMInfo(userId):
	headers = {'User-Agent': getUA()}
	r = requests.get(mmUrl+str(userId), timeout=5)
	# 检测响应内容的编码格式
	encoding = chardet.detect(r.content)['encoding']
	# 设置响应的编码方式，默认为'IOS-8859'
	r.encoding = encoding
	# 获取页面内容
	html = r.text
	r.close()      # 关闭响应
	replaceBR = re.compile(r'(<br.*?>)+|(\n)+|(\r)+|(\t)+')     # 处理<br>和换行符
	newhtml = re.sub(replaceBR, '  ', html)
	patt = '.*?昵.*?称.*?<span>(.*?)</span>.*?生.*?日.*?<span>.*?&nbsp;(.*?)</span>.*?' \
		'所在城市.*?<span>(.*?)</span>.*?职.*?业.*?<span>(.*?)</span>.*?血.*?型.*?<span>' \
		'(.*?)</span>.*?学校/专业.*?<span>(.*?)&nbsp;&nbsp;&nbsp;&nbsp;(.*?)</span>' \
		'.*?风.*?格.*?<span>(.*?)</span>.*?mm-p-height.*?<p>(.*?)</p>.*?mm-p-weight.*?' \
		'<p>(.*?)</p>.*?mm-p-size.*?<p>(.*?)</p>.*?mm-p-bar.*?<p>(.*?)</p>.*?mm-p-shose' \
		'.*?<p>(.*?)</p>.*?<!--经历开始-->.*?<p>(.*?)</p>.*?<!--经历结束-->.*?'
	result = [str(userId)] + list(re.findall(patt, newhtml)[0]) + [mmaishow+str(userId)]
	result[-2] = result[-2].strip()
	return result

if __name__ == '__main__':
	starttime = time.time()           # 获取程序开始时间
	totalPage = getTotalPage()
	with codecs.open(r'mmdetail.csv', 'w+', 'utf_8_sig') as fs:    # 如果没有newline参数的话，文件会多出许多空行
		csvwriter = csv.writer(fs, dialect='excel')        # excel数据文件

		print('开始获取数据...')
		'''
		列标题写入  淘女郎ID | 呢称 | 生日 | 所在城市 | 职业 | 血型 | 学校 | 专业 | 风格 | 身高(cm) | 体重(kg) | 
						三围 | 罩杯尺寸 | 穿鞋尺寸 | 经验 | 备注(打开获取联系方式)
		'''
		mmtitle = [
			'淘女郎ID', '昵称', '生日', '所在城市', '职业', '血型', 
			'学校', '专业', '风格', '身高(cm)', '体重(kg)', '三围',
			'罩杯尺寸', '穿鞋尺寸', '经验', '备注(打开获取联系方式)',
		]
		csvwriter.writerow(mmtitle)
		print()

		while cpage < totalPage:
			cpage += 1
			print('正在处理第%s页。。。' % cpage)
			try:
				mmList = getMMList(cpage)
			except:
				print('获取页数据失败！')
				pass
			if not mmList:  # 返回空值就是没有数据
				break
			mms = tqdm.tqdm(mmList, ascii=True, unit='users', postfix={'userId': 1})
			for mm in mms:
				mms.set_postfix(userId=str(mm['userId']), refresh=False)
				try:
					mminfo = getMMInfo(mm['userId'])
				except:
					failnum += 1
					pass
				csvwriter.writerow(mminfo)
				#print(str(count)+' ', end='')
				time.sleep(0.5)
				count += 1
			print('')
	
	endtime = time.time()         # 获取程序结束时间
	print('所有数据处理完毕--------共处理 {0} 条，失败 {1} 条，耗时 {2} s！'.format(count, failnum, (endtime-starttime)))