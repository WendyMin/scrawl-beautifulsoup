# -*- coding:utf-8 -*- #
'''
目前实现的功能：
1. 爬取http://www.265.com/，针对网站分类，提取各网站的名称和链接
2. 可以选择所要提取的分类
——————————————————————————————————————————————————————————————————————————————————————
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# 写入txt文档
def WriteFile(content):
	with open('265.txt', 'a') as f:
		f.write(content)
		f.write("\n")

# 用BeautifulSoup指定lxml解析器解析网页，得到一个文档的对象
def getPage(forumUrl):
	articleHtml = urlopen("http://www.265.com/"+forumUrl)
	articleBsObj = BeautifulSoup(articleHtml, "lxml")
	return articleBsObj

# 网址转换
def checkUrl(url):
	url = url.replace("%3A", ":")
	url = url.replace("%2F", "/")
	if re.search(re.compile("www."), url):
		a = url.split("www.")
		urltemp = "www." + a[len(a) - 1]
	else:
		if re.search(re.compile("http"), url):
			a = url.split("http")
			urltemp = "http" + a[len(a) - 1]
	if urltemp.endswith("/"):
		urltemp = urltemp[0:len(urltemp)-1]
	return urltemp

# 打印网站分类，各网站的名称和链接
def printWebSite(somethings):
	for onething in somethings:
		onethingUrl = onething.attrs["href"]
		onethingObj = getPage(onethingUrl)
		print(onething.get_text(), onethingUrl)
		WriteFile(onething.get_text()+" "+onethingUrl)
		webPages = onethingObj.findAll("span", {"class": "b-f-j"})
		for webPage in webPages:
			if not re.search(re.compile(r"相关搜索|分类目录"), str(webPage)):		# 不包含相关搜索或分类目录
				print(webPage.get_text())
				WriteFile(webPage.get_text())
				page1 = webPage.parent.parent.nextSibling.a.parent
				print(page1.a.get_text(), ":", checkUrl(page1.a.attrs["href"]))
				WriteFile(page1.a.get_text()+":"+page1.a.attrs["href"])
				pageNext = page1.nextSibling
				while pageNext != None:
					if re.search(re.compile("^(http)"), pageNext.a.attrs["href"]):  # 天气->湛江 的网址不对
						print(pageNext.get_text(), ":", checkUrl(pageNext.a.attrs["href"]))
						WriteFile(pageNext.get_text()+":"+pageNext.a.attrs["href"])
					pageNext = pageNext.nextSibling

# 生活服务分类
def Life():
	life = bsObj.find("span", text="生活服务")
	services = life.parent.parent.nextSibling.findAll("a", {"site-c-action": "c-category-life-click"})
	print("【生活服务类】")
	WriteFile("【生活服务类】")
	printWebSite(services)

# 休闲娱乐分类
def Relax():
	relax = bsObj.find("span", text="休闲娱乐")
	entertainments = relax.parent.parent.nextSibling.findAll("a", {"site-c-action": "c-category-relax-click"})
	print("【休闲娱乐类】")
	WriteFile("【休闲娱乐类】")
	printWebSite(entertainments)

# 其他分类
def Other():
	other = bsObj.find("span", text="其他")		# 找到其他分类
	otherthings = other.parent.parent.nextSibling.findAll("a", {"site-c-action": "c-category-other-click"})
	print("【其他】")
	WriteFile("【其他】")
	printWebSite(otherthings)


if __name__ == '__main__':
	html = urlopen("http://www.265.com/")
	bsObj = BeautifulSoup(html.read(), "lxml")					# 用BeautifulSoup指定lxml解析器解析

	choice1 = input("请选择 1.生活服务 2.休闲娱乐 3.其他 (输入数字即可)(回车默认全选)：")
	if choice1.strip() == "":
		Life()
		Relax()
		Other()
	else:
		if int(choice1) == 1:
			Life()
		if int(choice1) == 2:
			Relax()
		if int(choice1) == 3:
			Other()

