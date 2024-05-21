from glob import glob
from sklearn.model_selection import train_test_split

cats = glob('train/Cat/*.jpg')
dogs = glob('train/Dog/*.jpg')

cats_train, cats_test = train_test_split(cats, test_size=0.30)
dogs_train, dogs_test = train_test_split(dogs, test_size=0.30)

TRAIN_DIR = 'train'
TEST_DIR = 'test'

# Jupyter`
# !mkdir test

# !mkdir test/Cat
files = ' '.join(cats_test)
# !mv -t test/Cat $files

# !mkdir test/Dog
files = ' '.join(dogs_test)
# !mv -t test/Dog $files
