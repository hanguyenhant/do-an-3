import gensim
from gensim import corpora

class LDA:
	def load_data(self, path):
		self._data = []
		with open(path, encoding="utf-8") as f:
			lines = f.read().splitlines()
		for line in lines:
			content = line.split('<fff>')[1]
			self._data.append([word for word in content.split()])

	def create_dictionary(self):
		self._dictionary = corpora.Dictionary(self._data)
		self._dictionary.filter_extremes(no_below=10, no_above=.9)
		# print(dictionary)

	def implement_lda(self):
		corpus = [self._dictionary.doc2bow(doc) for doc in self._data]
		# print(corpus[6])
		model = gensim.models.LdaModel(corpus,
								id2word=self._dictionary,
								num_topics=10,
								passes=10,
								iterations=100,
								decay=0.7,
								offset=10.1)
		topics = model.show_topics(num_topics=10, num_words=10, formatted=False)
		for topic_index, term_list in topics:
			print('\ntopic {}\n'.format(topic_index+1))
			for term, value in term_list:
				print(term)
	
lda = LDA()
lda.load_data('clean_data.txt')
# print(lda._data[:10])
lda.create_dictionary()
lda.implement_lda()
