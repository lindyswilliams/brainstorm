import numpy as np
import struct

def load_data(labels, images):
    arr = []
    # load into numpy arrays
    with open(labels, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(images, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)
    
    get_img = lambda idx: (lbl[idx], img[idx])

    for i in xrange(len(lbl)):
        arr.extend([get_img(i)])
    return arr

# training
fname_lbl1 = "/Users/lindywilliams/Documents/Data/MNIST/train-labels-idx1-ubyte"
fname_img1 = "/Users/lindywilliams/Documents/Data/MNIST/train-images-idx3-ubyte"
train = load_data(fname_lbl1, fname_img1)

training = []
for i in range(0, len(train)):
    training.append((train[i][0], (train[i][1].reshape([1,784]))))

# testing
fname_lbl2 = "/Users/lindywilliams/Documents/Data/MNIST/t10k-labels-idx1-ubyte"
fname_img2 = "/Users/lindywilliams/Documents/Data/MNIST/t10k-images-idx3-ubyte"
test = load_data(fname_lbl2, fname_img2)

testing = []
for i in range(0, len(test)):
    testing.append((test[i][0], (test[i][1].reshape([1,784]))))

class Element():
	def __init__(self, idx, dist):
		self.idx = idx
		self.dist = dist

	def __repr__(self):
		return "Element(%s, %s)" % (self.idx, self.dist)

class Container():
	def __init__(self, test_label):
		self.test_label = test_label
		self.elements = []

	def add_element(self, element):
		self.elements.append(element)

	def closest_k(self, k):
		return sorted(self.elements, key=lambda e: e.dist)[:k]


for test in testing[:1]: 
	c = Container(test[0])
	for train in training[:10000]:
		dist = numpy.linalg.norm(train[1]-test[1])
		c.add_element(Element(train[0], dist))


