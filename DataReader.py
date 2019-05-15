import re, string
from pyvi import ViTokenizer, ViPosTagger
import pymysql.cursors 

class DataReader:
	def connect_database(self):
		#1. Kết nối vào database
		
		self._connection = pymysql.connect(host='127.0.0.1',
				                             user='root',
				                             password='123456',                             
				                             db='baiviet',
				                             charset='utf8',
				                             )
		try:
			with self._connection.cursor() as cursor:
				# Create a new record
				sql = """SELECT the_loai, noi_dung FROM bai_viet"""
				cursor.execute(sql)
				self._result = cursor.fetchall()
		finally:
			self._connection.close()

	def load_topics(self):
		self._topics = []
		topics = set()
		for doc in self._result:
			topics.add(doc[0])
		self._topics = sorted(topics)
		# print(self._topics)

	def clean_data(self):
		self._data = []

		for doc in self._result:
			# print(doc[0])
			label = self._topics.index(doc[0])
			# print(label)

			words = str(doc[1])
			words = words.replace('\n',' ')

			#Loại bỏ ký tự đặc biệt và ký tự số		
			words = re.sub(r'[^\w\s]','', str(words), re.UNICODE)
			words = re.sub(r'(\b\d+\b)','', str(words), re.UNICODE)

			#Tách từ
			doc_clean = ViTokenizer.tokenize(words)
			doc_clean = doc_clean.lower()
			doc_clean = doc_clean.split()

			#Loại bỏ stop words
			stop_words = list()
			f = open("vietnamese-stopwords-dash.txt", mode="r", encoding="utf-8")
			for line in f:
				stop_words.append(line[:-1]); #bỏ \n ở cuối từ
			f.close()

			words = [word for word in doc_clean if word not in stop_words and word not in string.punctuation]
			content = ' '.join(words)

			# print(content)
			self._data.append(str(label) + '<fff>' + content)
	
	def save_text_processed(self, path):
		with open(path, 'w', encoding="utf-8") as f:
			f.write('\n'.join(self._data))
		


		



