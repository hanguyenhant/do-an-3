import pymysql.cursors
import feedparser
from urllib.request import urlopen
from bs4 import BeautifulSoup

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
					'https://vnexpress.net/rss/oto-xe-may.rss', 'https://vnexpress.net/rss/suc-khoe.rss', 
					'https://vnexpress.net/rss/khoa-hoc.rss', 'https://vnexpress.net/rss/du-lich.rss']
		# count=0
		for link_rss in list_rss:
			d = feedparser.parse(link_rss)
			the_loai = link_rss.split('/')[4].split('.')[0]
			if the_loai == 'so-hoa':
				the_loai = 'cong-nghe'
			if the_loai == 'oto-xe-may':
				the_loai = 'xe'

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
					# print(contentString)
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
					html = urlopen(post.link)
					bsObj = BeautifulSoup(html.read(), "html.parser")
					content = bsObj.find("div", {"class":"ArticleContent"}).findAll('p')
					
					contentList = list()
					for i in range(len(content)-1):
						contentList.append(content[i].get_text())

					contentString = " ".join(contentList)
					# print(contentString)
					if contentString != "":
						self._baivietList.append([the_loai, post.title, contentString, post.link])


	def collect_data_from_tuoitre(self):
		list_rss = ['https://tuoitre.vn/rss/the-gioi.rss', 'https://tuoitre.vn/rss/the-thao.rss', 
					'https://tuoitre.vn/rss/phap-luat.rss', 'https://tuoitre.vn/rss/kinh-doanh.rss', 
					'https://tuoitre.vn/rss/nhip-song-so.rss', 'https://tuoitre.vn/rss/giao-duc.rss', 
					'https://tuoitre.vn/rss/xe.rss', 'https://tuoitre.vn/rss/suc-khoe.rss', 
					'https://tuoitre.vn/rss/khoa-hoc.rss', 'https://tuoitre.vn/rss/du-lich.rss']

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

	def load_data_from_database(self):
		self.connect_database()
		try:
			with self._connection.cursor() as cursor:
				sql = """SELECT duong_dan FROM data_bai_viet"""
				cursor.execute(sql)
				self._result = cursor.fetchall()
		finally:
			self._connection.close()

	def save_to_database(self):
		self.connect_database()
		#3. lưu vào CSDL
		try:
			with self._connection.cursor() as cursor:
				sql = """INSERT INTO `data_bai_viet` (`the_loai`, `tieu_de`, `noi_dung`, `duong_dan`) VALUES (%s, %s, %s, %s)"""
				for baiviet in self._baivietList:
					if (baiviet[0], baiviet[1], baiviet[2], baiviet[3]) not in self._result:
						cursor.execute(sql,(baiviet[0], baiviet[1], baiviet[2], baiviet[3]))

			    # connection is not autocommit by default. So you must commit to save
			    # your changes.
				self._connection.commit()
		finally:
			self._connection.close()