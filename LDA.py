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

	def implement_lda(self):
		doc_term_matrix = [self._dictionary.doc2bow(doc) for doc in self._data]

		Lda = gensim.models.ldamodel.LdaModel

		ldamodel = Lda(doc_term_matrix, num_topics=8, id2word = self._dictionary, passes=50)

		print(ldamodel.print_topics(num_topics=8, num_words=5))

	
lda = LDA()
lda.load_data('clean_data.txt')
lda.create_dictionary()
lda.implement_lda()
