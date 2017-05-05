# -*- coding:utf-8 -*- #
'''
目前实现的功能：
1. 可提取论坛各版块名称、板块内帖子的标题、发帖人、时间，并根据回帖线索串联帖子
2. 可自定义提取的版块名称、版块内爬取深度，以及帖子爬取深度
——————————————————————————————————————————————————————————————————————————————————————
'''


from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# 用BeautifulSoup指定lxml解析器解析网页，得到一个文档的对象
def getPage(forumUrl):
	articleHtml = urlopen("http://bbs.tianya.cn"+forumUrl)
	articleBsObj = BeautifulSoup(articleHtml, "lxml")
	return articleBsObj

# 在每个版块界面，打印title,author,time信息，并进入每一个帖子，调用getPostData函数打印帖子具体内容
# 并返回下一页url（不含http://bbs.tianya.cn）
def getPostInf(eachForumUrl, postDeep):
	titles = eachForumUrl.findAll("td", {"class": "td-title faceblue"})		# 找到标题位置
	for title in titles:
		author = title.nextSibling.nextSibling									# 作者
		time = author.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling		# 最新回复时间
		print("【帖子链接】:", title.a.attrs['href'])		# 帖子链接（不含http://bbs.tianya.cn）
		print("title :", (title.get_text().strip()))
		print("author:", (author.get_text()))
		print("time  :", (time.get_text()))
		posturl = title.a.attrs['href']					# 帖子链接（不含http://bbs.tianya.cn）
		getpostdata = "yep"
		postDeepNow = 1
		while (getpostdata != None) and (postDeepNow != (postDeep + 1)):
			print("帖子第", postDeepNow, "页：")
			postDeepNow += 1
			getpostdata = getPostData(posturl)			# 调用getPostData函数，根据回帖线索串联帖子
			posturl = getpostdata
	nextPage = eachForumUrl.find("a", href=re.compile("nextid"))
	nextPageUrl = nextPage.attrs['href']  				# 下一页链接（不含http://bbs.tianya.cn）
	return nextPageUrl

# 打印帖子的发帖人、主帖、回帖人、回帖
def getPostData(postUrl):
	postbsObj = getPage(postUrl)
	if postbsObj.find("div", {"class": "atl-info"}) != None:								# 如果是网页格式正确（有极个别网页乱码）
		postAuthor = postbsObj.find("div", {"class": "atl-info"}).span.a.attrs['uname']		# 发帖人
		postArticle = postbsObj.find("div", {"class": "bbs-content clearfix"})				# 1楼（主帖）
		posters = postbsObj.find_all("div", {"class": "atl-info"})							# 所有帖子
		if postArticle != None:																# 如果是主帖，打印出来
			print(postAuthor, ":", postArticle.get_text().strip())
		t = 0
		for poster in posters:							# 跳过第一个无效的poster
			if t != 0:
				posterName = poster.span.a.attrs['uname']
				postContent = poster.parent.nextSibling.nextSibling.find("div", {"class": "bbs-content"})
				print(posterName, ":", postContent.get_text().strip())
			t = 1
		if postbsObj.find("a", {"class": "js-keyboard-next"}) != None:						# 如果有下一页
			nextPageUrl = postbsObj.find("a", {"class": "js-keyboard-next"}).attrs['href']		# 下一页链接（不含http://bbs.tianya.cn）
			return nextPageUrl
	else:
		return None

if __name__ == '__main__':
	html = urlopen("http://bbs.tianya.cn/")
	bsObj = BeautifulSoup(html.read(),"lxml")						# 用BeautifulSoup指定lxml解析器解析

	forumList = bsObj.findAll("a", {"class": "child_link"}, href=re.compile("^(?!(http))"))		# 找到各版块
	for forum in forumList:
		print(forum.get_text())										# 各版块名称

	forumName = input("请输入所要查询版块名称（按回车默认全部）：")
	forumDeep = input("请输入版块深度（论坛版块前几页）：")
	postDeep = input("请输入帖子深度（最多到前几页）：")

	if forumDeep.strip() == "":										# 如果没输入，默认版块深度为1
		forumDeep = 1
	if postDeep.strip() == "":										# 如果没输入，默认帖子深度为3
		postDeep = 3

	if forumName.strip() == "":										# 默认全部版块
		for forum in forumList:
			print(forum.get_text())  								# 版块名称
			eachForumUrl = getPage(forum.attrs['href'])  			# 版块链接（含http://bbs.tianya.cn）
			for i in range(int(forumDeep)):
				print("版块第", i + 1, "页：")
				nextPage = getPostInf(eachForumUrl, int(postDeep))  # 下一页链接（不含http://bbs.tianya.cn）
				eachForumUrl = getPage(nextPage)
	else:															# 选定某一版块时
		for forum in forumList:
			if forum.get_text() == forumName:
				print(forum.get_text())  							# 版块名称
				eachForumUrl = getPage(forum.attrs['href'])			# 版块链接（含http://bbs.tianya.cn）
				for i in range(int(forumDeep)):
					print("版块第", i+1, "页：")
					nextPage = getPostInf(eachForumUrl, int(postDeep))		# 下一页链接（不含http://bbs.tianya.cn）
					eachForumUrl = getPage(nextPage)

