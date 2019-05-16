import pymysql.cursors
import feedparser
from urllib.request import urlopen
from urllib.request import build_opener
from bs4 import BeautifulSoup
from http.client import IncompleteRead

class DataCollection:
	def __init__(self):
		self._baivietList = list()

	def connect_database(self):
		#1. Kết nối vào database
		 
		self._connection = pymysql.connect(host='127.0.0.1',
		                             user='root',
		                             password='123456',                             
		                             db='baiviet',
		                             charset='utf8',
		                             )
		
	def collect_data_from_vnexpress(self):
		#2. Lấy link rss và thể loại - tiêu đề - nội dung - link bài viết.
		#==> Lưu vào CSDL
		list_rss = ['https://vnexpress.net/rss/the-gioi.rss', 'https://vnexpress.net/rss/the-thao.rss', 
					'https://vnexpress.net/rss/phap-luat.rss', 'https://vnexpress.net/rss/kinh-doanh.rss', 
					'https://vnexpress.net/rss/so-hoa.rss', 'https://vnexpress.net/rss/giao-duc.rss', 
					'https://vnexpress.net/rss/suc-khoe.rss', 'https://vnexpress.net/rss/du-lich.rss']
		# count=0
		for link_rss in list_rss:
			d = feedparser.parse(link_rss)
			the_loai = link_rss.split('/')[4].split('.')[0]
			if the_loai == 'so-hoa':
				the_loai = 'cong-nghe'

			for post in d.entries:
				if hasattr(post, 'link'):
					# count+=1
					# print("\n%d. %s - %s: %s" % (count, the_loai, post.title, post.link))
					html = urlopen(post.link)
					bsObj = BeautifulSoup(html.read(), "html.parser")
					content = bsObj.findAll("p", {"class":"Normal"})
					contentList = list()
					for i in range(len(content)-1):
						contentList.append(content[i].get_text())

					contentString = " ".join(contentList)
					if len(contentString) > 21000:
						contentString = contentString[:21000]
					if contentString != "":
						self._baivietList.append([the_loai, post.title, contentString, post.link])
	
	def collect_data_from_vietnamnet(self):
		list_rss = ['https://vietnamnet.vn/rss/the-gioi.rss', 'https://vietnamnet.vn/rss/the-thao.rss', 
					'https://vietnamnet.vn/rss/phap-luat.rss', 'https://vietnamnet.vn/rss/kinh-doanh.rss', 
					'https://vietnamnet.vn/rss/cong-nghe.rss', 'https://vietnamnet.vn/rss/giao-duc.rss', 
					'https://vietnamnet.vn/rss/suc-khoe.rss']

		for link_rss in list_rss:
			d = feedparser.parse(link_rss)
			the_loai = link_rss.split('/')[4].split('.')[0]

			for post in d.entries:
				if hasattr(post, 'link'):
					opener = build_opener()
					opener.addheaders = [('User-agent', 'Mozilla/5.0')]
					html = opener.open(post.link)
					bsObj = BeautifulSoup(html.read(), "html.parser")
					
					content = bsObj.find("div", {"class":"ArticleContent"}).findAll('p')
					
					contentList = list()
					for i in range(len(content)-1):
						contentList.append(content[i].get_text())

					contentString = " ".join(contentList)
					if len(contentString) > 21000:
						contentString = contentString[:21000]
					if contentString != "":
						self._baivietList.append([the_loai, post.title, contentString, post.link])

	def collect_data_from_tuoitre(self):
		list_rss = ['https://tuoitre.vn/rss/the-gioi.rss', 'https://tuoitre.vn/rss/the-thao.rss', 
					'https://tuoitre.vn/rss/phap-luat.rss', 'https://tuoitre.vn/rss/kinh-doanh.rss', 
					'https://tuoitre.vn/rss/nhip-song-so.rss', 'https://tuoitre.vn/rss/giao-duc.rss', 
					'https://tuoitre.vn/rss/suc-khoe.rss', 'https://tuoitre.vn/rss/du-lich.rss']

		for link_rss in list_rss:
			d = feedparser.parse(link_rss)
			the_loai = link_rss.split('/')[4].split('.')[0]
			if the_loai == 'nhip-song-so':
				the_loai = 'cong-nghe'

			for post in d.entries:
				if hasattr(post, 'link'):
					# count+=1
					# print("\n%d. %s - %s: %s" % (count, the_loai, post.title, post.link))
					html = urlopen(post.link)
					bsObj = BeautifulSoup(html.read(), "html.parser")

					if bsObj.find("div", {"id":"main-detail-body"}) != None:
						content = bsObj.find("div", {"id":"main-detail-body"}).findAll('p')

					contentList = list()
					for i in range(len(content)-1):
						contentList.append(content[i].get_text())

					contentString = " ".join(contentList)
					# print(contentString)
					if len(contentString) > 21000:
						contentString = contentString[:21000]
					if contentString != "":
						self._baivietList.append([the_loai, post.title, contentString, post.link])

	def collect_data_from_24h(self):
		#2. Lấy link rss và thể loại - tiêu đề - nội dung - link bài viết.
		#==> Lưu vào CSDL
		list_rss = ['https://www.24h.com.vn/upload/rss/thethao.rss', 'https://www.24h.com.vn/upload/rss/bongda.rss', 
					'https://www.24h.com.vn/upload/rss/congnghethongtin.rss', 'https://www.24h.com.vn/upload/rss/suckhoedoisong.rss', 
					'https://www.24h.com.vn/upload/rss/dulich24h.rss', 'https://www.24h.com.vn/upload/rss/giaoducduhoc.rss',
					'https://www.24h.com.vn/upload/rss/anninhhinhsu.rss', 'https://www.24h.com.vn/upload/rss/taichinhbatdongsan.rss']
		# count=0
		for link_rss in list_rss:
			d = feedparser.parse(link_rss)
			the_loai = link_rss.split('/')[5].split('.')[0]
			if the_loai == 'bongda' or 'thethao':
				the_loai = 'the-thao'
			if the_loai == 'giaoducduhoc':
				the_loai = 'giao-duc'
			if the_loai == 'congnghethongtin':
				the_loai = 'cong-nghe'
			if the_loai == 'dulich24h':
				the_loai = 'du-lich'
			if the_loai == 'suckhoedoisong':
				the_loai = 'suc-khoe'
			if the_loai == 'taichinhbatdongsan':
				the_loai = 'kinh-doanh'
			if the_loai == 'anninhhinhsu':
				the_loai = 'phap-luat'

			for post in d.entries:
				if hasattr(post, 'link'):
					# count+=1
					# print("\n%d. %s - %s: %s" % (count, the_loai, post.title, post.link))
					html = urlopen(post.link)
					bsObj = BeautifulSoup(html.read(), "html.parser")

					if bsObj.find("article", {"class":"nwsHt nwsUpgrade"}) != None:
						content = bsObj.find("article", {"class":"nwsHt nwsUpgrade"}).findAll('p')

					contentList = list()
					for i in range(len(content)-1):
						contentList.append(content[i].get_text())

					contentString = " ".join(contentList)
					if len(contentString) > 21000:
						contentString = contentString[:21000]
					if contentString != "":
						self._baivietList.append([the_loai, post.title, contentString, post.link])

	def collect_data_from_thanhnien(self):
		list_rss = ['https://thanhnien.vn/rss/the-gioi/goc-nhin.rss', 'https://thanhnien.vn/rss/viet-nam/phap-luat.rss',  
					'https://thanhnien.vn/rss/giao-duc/du-hoc.rss', 'https://thanhnien.vn/rss/giao-duc/tuyen-sinh.rss',
					'https://thanhnien.vn/rss/giao-duc/nguoi-thay.rss', 'https://thanhnien.vn/rss/giao-duc/chon-nghe.rss',
					'https://thanhnien.vn/rss/cong-nghe-thong-tin/san-pham-moi.rss', 'https://thanhnien.vn/rss/cong-nghe/xu-huong.rss',
					'https://thanhnien.vn/rss/cong-nghe-thong-tin/y-tuong.rss', 'https://thanhnien.vn/rss/cong-nghe-thong-tin/kinh-nghiem.rss',
					'https://thanhnien.vn/rss/suc-khoe/lam-dep.rss', 'https://thanhnien.vn/rss/doi-song/gioi-tinh.rss',
					'https://thanhnien.vn/rss/suc-khoe/khoe-dep-moi-ngay.rss', 'https://thanhnien.vn/rss/suc-khoe/yeu-da-day.rss',
					]

		for link_rss in list_rss:
			d = feedparser.parse(link_rss)
			the_loai = link_rss.split('/')[5].split('.')[0]
			if the_loai == 'goc-nhin':
				the_loai = 'the-gioi'
			if the_loai == 'du-hoc' or 'tuyen-sinh' or 'chon-truong' or 'nguoi-thay' or 'chon-nghe':
				the_loai = 'giao-duc'
			if the_loai == 'san-pham-moi' or 'xu-huong' or 'y-tuong' or 'kinh-nghiem':
				the_loai = 'cong-nghe'
			if the_loai == 'lam-dep' or 'gioi-tinh' or 'khoe-dep-moi-ngay' or 'yeu-da-day':
				the_loai = 'suc-khoe'

			for post in d.entries:
				if hasattr(post, 'link'):
					# count+=1
					# print("\n%d. %s - %s: %s" % (count, the_loai, post.title, post.link))
					html = urlopen(post.link)
					bsObj = BeautifulSoup(html.read(), "html.parser")

					if bsObj.find("div", {"id":"abody"}) != None:
						content = bsObj.find("div", {"id":"abody"}).findAll('div')

					contentList = list()
					for i in range(len(content)-1):
						contentList.append(content[i].get_text())

					contentString = " ".join(contentList)
					# print(contentString)
					if len(contentString) > 21000:
						contentString = contentString[:21000]
					if contentString != "":
						self._baivietList.append([the_loai, post.title, contentString, post.link])

	def collect_data_from_nguoilaodong(self):
		list_rss = ['https://nld.com.vn/thoi-su-quoc-te.rss', 'https://nld.com.vn/kinh-te.rss',  
					'https://nld.com.vn/phap-luat.rss', 'https://nld.com.vn/the-thao.rss', 
					'https://nld.com.vn/cong-nghe-thong-tin.rss', 'https://nld.com.vn/suc-khoe.rss',
					'https://nld.com.vn/giao-duc-khoa-hoc.rss'
					]

		for link_rss in list_rss:
			d = feedparser.parse(link_rss)
			the_loai = link_rss.split('/')[3].split('.')[0]
			if the_loai == 'thoi-su-quoc-te':
				the_loai = 'the-gioi'
			if the_loai == 'kinh-te':
				the_loai = 'kinh-doanh'
			if the_loai == 'cong-nghe-thong-tin':
				the_loai = 'cong-nghe'
			if the_loai == 'giao-duc-khoa-hoc':
				the_loai = 'giao-duc'

			for post in d.entries:
				if hasattr(post, 'link'):
					# count+=1
					# print("\n%d. %s - %s: %s" % (count, the_loai, post.title, post.link))
					
					opener = build_opener()
					opener.addheaders = [('User-agent', 'Mozilla/5.0')]
					html = opener.open(post.link)
					bsObj = BeautifulSoup(html.read(), "html.parser")

					if bsObj.find("div", {"id":"divNewsContent"}) != None:
						content = bsObj.find("div", {"id":"divNewsContent"}).findAll('p')

					contentList = list()
					for i in range(len(content)-1):
						contentList.append(content[i].get_text())

					contentString = " ".join(contentList)
					# print(contentString)
					if len(contentString) > 21000:
						contentString = contentString[:21000]
					if contentString != "":
						self._baivietList.append([the_loai, post.title, contentString, post.link])

	def save_to_database(self):
		#3. lưu vào CSDL
		try:
			with self._connection.cursor() as cursor:
				sql = """INSERT INTO `bai_viet` (`the_loai`, `tieu_de`, `noi_dung`, `duong_dan`) VALUES (%s, %s, %s, %s)"""
				for baiviet in self._baivietList:
					cursor.execute(sql,(baiviet[0], baiviet[1], baiviet[2], baiviet[3]))

				self._connection.commit()
		finally:
			self._connection.close()