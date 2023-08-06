from gcpds.utils import loaddb

db = loaddb.BCI_CIV_2a()
db.load_subject(3)
d, c = db.get_data()
d
# data, classes = db.get_data(classes=['noise-200', 'music-50'])
# non_task = db.non_task()
# epochs = db.get_epochs()

