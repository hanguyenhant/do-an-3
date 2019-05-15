from DataCollection import DataCollection
from DataReader import DataReader

data_collection = DataCollection()
data_collection.load_data_from_database()
data_collection.collect_data_from_vnexpress()
# data_collection.collect_data_from_vietnamnet()
# data_collection.collect_data_from_tuoitre()

data_collection.save_to_database()

# data_reader = DataReader()
# data_reader.connect_database()
# data_reader.load_topics()
# data_reader.clean_data()
# data_reader.save_text_processed('clean_data.txt')