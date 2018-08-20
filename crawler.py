# coding = utf-8
from lxml import etree
import requests
import regex as re
import numpy as np
# 构建双色球期数的列表，从03001开始
path = '/periods.html'
html_file = open(path, 'r').read()

re_data = re.findall(r'>\d{5}<', html_file)
periods = []
for data in re_data:
	periods.append(data[1:6])
periods.reverse()
periods_length = len(periods)
winning_numbers = []
i_step = 0
for index in periods:
	url = 'http://kaijiang.500.com/shtml/ssq/' + index + '.shtml'
	response = requests.get(url)
	response.encoding = 'gb18030'
	xpath = etree.HTML(response.text)
	numbers = xpath.xpath('//div[@class="ball_box01"]/ul/li')
	winning_number = []
	for number in numbers:
		# numbers返回的是一个字典
		winning_number.append(number.text)
	winning_numbers.append(winning_number)
	i_step += 1
	left_percent = (1-i_step/periods_length)*100
	print('正在爬取双色球第' + str(index) + '期开奖号码, -----------------剩余' + str(left_percent) + '%')
np.save('lottery', winning_numbers)
print(winning_numbers)

