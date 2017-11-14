# scrawl-beautifulsoup

![](https://img.shields.io/badge/Python-3.6.1-blue.svg?style=flat)
![](https://img.shields.io/badge/BeautifulSoup-4.5.3-brightgreen.svg?style=flat) 
![](https://img.shields.io/badge/lxml-3.7.3-green.svg?style=flat)
![](https://img.shields.io/badge/Selenium-3.4.1-yellow.svg?style=flat) 
![](https://img.shields.io/badge/Webdriver-PhantomJS-orange.svg?style=flat)
![](https://img.shields.io/badge/Chorme--red.svg?style=flat)

[Beautiful Soup 4.4.0 文档](http://beautifulsoup.readthedocs.io/zh_CN/latest/)

[Selenium with Python中文翻译文档](http://selenium-python-zh.readthedocs.io/en/latest/index.html)


## 论坛 ##
[天涯](http://bbs.tianya.cn)

目前实现的功能：

1. 可提取论坛各版块名称、板块内帖子的标题、发帖人、时间，并根据回帖线索串联帖子

2. 可自定义提取的版块名称、版块内爬取深度，以及帖子爬取深度

## 导航网站 ##
[谷歌265](http://www.265.com/)

目前实现的功能：

1. 针对网站分类，提取各网站的名称和链接

2. 可以选择所要提取的分类

## 网购网站 ##
[淘宝](https://www.taobao.com/)

目前实现的功能：

1. 在各商品分类下提取商品名称、价格、评价总数、各类评价数量

有待改进的地方：

1. 有些大分类下的网站格式不同（童装玩具、孕产、用品），用js加载类目，还有些（尤其是后面的分类网页）也不符合查找的格式，无法用`<dl class="theme-bd-level2">`找出，需要进行对应修改

2. 有些url对中文没有正确编码，无法用urlopen直接打开，需要改进encode,decode函数

3. 在查找累计评论数的时候，没有用WebDriverWait函数，而是直接time.sleep了2秒钟，有待改进


-------
另：

1. 本项目采用Selenium在后台打开无头浏览器进行动态数据的爬取，因此速度相对post表单来说较慢，可以尝试将Selenium改为post，加快爬取速度

2. 可以采用scrapy进行多线程爬取

3. 可以将爬取数据记录到Redis或者其他数据库中


5/2/2017 9:50:30 PM 
