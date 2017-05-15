# -*- coding:utf-8 -*- #
'''
目前实现的功能：
1. 在各商品分类下提取商品名称、价格、评价总数、各类评价数量

有待改进的地方：
1. 有些大分类下的网站格式不同（童装玩具、孕产、用品）,用js加载类目，还有些（尤其是后面的分类网页）也不符合查找的格式，无法用<dl class="theme-bd-level2">找出，需要进行对应修改
2. 有些url对中文没有正确编码，无法用urlopen直接打开，需要改进encode,decode函数
3. 在查找累计评论数的时候，没有用WebDriverWait函数，而是直接time.sleep了2秒钟，有待改进
# ——————————————————————————————————————————————————————————————————————————————————————
'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pages = set()																	# 防止网页链接重复

# 用BeautifulSoup指定lxml解析器解析网页，得到一个文档的对象
def getPage(url):
	html = urlopen(url)
	bsObj = BeautifulSoup(html, "lxml")
	return bsObj

# 如果url不符合规范，加上https:
def checkUrl(url):
	if re.search(re.compile("^(https).*"), str(url)):
		href = str(url)
	else:
		href = str("https:" + url)
	return href

# 找到首页下商品分类，调用getSmallCategoryUrl函数，打印分类
# 目前就从女装到配件
def getCategoryUrl(bsObj):
	global pages
	categories = bsObj.find("ul", {"class": "service-bd"}).findAll("a")			# 找到首页下每个商品分类
	for category in categories:
		if category.get_text() == "童装玩具":										# 先到童装玩具部分截止
			return None
		else:
			categoryHref = checkUrl(category.attrs['href'])
			if categoryHref not in pages and category.get_text() != "手机":  	# 户外、生鲜、零食、用品的url重复，手机与数码页面分类内容一模一样，过滤
				pages.add(categoryHref)
				print("【", category.get_text(), "】")							# 打印商品分类
				# print(categoryHref)											# 打印商品分类跳转页面
				getSmallCategoryUrl(categoryHref)

# 找到每个大分类下的小分类，调用getGoods函数
def getSmallCategoryUrl(CategoryUrl):
	SmallCategoryBsObj = getPage(CategoryUrl)
	smallcategories = SmallCategoryBsObj.findAll("dl", {"class": "theme-bd-level2"})		# 找到大分类下小分类位置
	for smallcategory in smallcategories:
		smallcategoryGroup = smallcategory.findAll("a")
		for smallCategoryReal in smallcategoryGroup:									# 找到每个小分类
			print("[", smallCategoryReal.get_text(), "]")
			smallCategoryRealHref = checkUrl(smallCategoryReal.attrs['href'])
			try:
				pageBsObj = getPage(smallCategoryRealHref)
				getGoods(smallCategoryRealHref)
			except:
				print("getSmallCategoryUrl error")

# 打印商品信息
def getGoods(url):
	driver = webdriver.PhantomJS()
	driver.get(url)
	pagesource = driver.page_source
	goodsBsObj = BeautifulSoup(pagesource, "lxml")
	details = goodsBsObj.findAll("div", {"class": "item J_MouserOnverReq item-sku J_ItemListSKUItem"})
	for detail in details:
		print("商品名称", detail.img.attrs['alt'])  							# 商品名称
		print("价格:", detail.a.attrs['trace-price'])  						# 价格
		goodHref = checkUrl(detail.a.attrs['href'])
		print(goodHref)
		driver.get(goodHref)
		time.sleep(2)
		button = driver.find_element_by_xpath("//a[@shortcut-key='g c']")			# 累计评论
		print(button.text)
		button.click()
		try:
			element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "reviews-t-val1")))
			haoping = driver.find_element_by_xpath("//label[@for='reviews-t-val1']")  # 好评
			print(haoping.text)
			zhongping = driver.find_element_by_xpath("//label[@for='reviews-t-val0']")  # 中评
			print(zhongping.text)
			chaping = driver.find_element_by_xpath("//label[@for='reviews-t-val-1']")  # 差评
			print(chaping.text)
		except:
			print("getGoods error")

if __name__ == '__main__':
	bsObj = getPage("https://www.taobao.com/")
	getCategoryUrl(bsObj)