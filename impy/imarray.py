from .__imports__ import *

class imarray(object):
	#Class to handle Image Objects
	#Usage:
	#	img = imarray(path)
	#		OR
	#	img = imarray(path,'RGB')
	def __init__(self,path=None,mode='L'):
		if path == None:
			return
		try :
			self.__image = imread(path, mode = mode)

		except :
			print("Error! Could not read the image from the path specified: %s"%path)
			return
		try :
			self.__image = np.asarray(self.__image)
			self.__dimension = self.__image.shape
			self.__type = path.split(".")[-1]
		except :
			print("Internal Error! Image file not supported")

	def __repr__(self):
		#Method to return the image value when an object of the class is created
		#	img = imarray(path)
		#	img store the image. Not the
		return repr(self.__image)

	def __cmp__(self,img):
		return cmp(self,img)

	def __getitem__(self,coordinates):
		return self.__image[coordinates]

	def load(self, image) :
		image = np.asarray(image,dtype=np.uint8)
		if len(image.shape) == 2 :
			self.__image = image
			try :
				self.__dimension = self.__image.shape
			except :
				print("Internal Error! Image file not supported")
		else :
			print("Assignment Error. Given input is not an image")

	def getShape(self):
		return self.__dimension
	shape = property(getShape)

	def getExtension(self):
		return self.__type
	ext = property(getExtension)

	def displayImage(self,mode='Greys_r'):
		try:
			plt.imshow(self.__image,cmap=mode)
		except:
			print("Image could not be displayed")
			return
		plt.show()
	disp = property(displayImage)

	def save(self,name):
		plt.imsave(name,self.__image)

	def convolve(self,mask):
		mask = np.asarray(mask,dtype=np.float32)
		if len(mask.shape) != len(self.__dimension):
			print("Invalid Mask Dimensions")
		(m,n) = mask.shape
		padY = int(np.floor(m/2))
		padX = int(np.floor(n/2))
		(M,N) = self.__dimension
		padImg = np.ones((M+padY*2,N+padX*2))*128
		fImage = np.zeros((M+padY*2,N+padX*2))
		padImg[padY:-padY,padX:-padX] = self.__image

		for yInd in range(padY,M+padY):
			for xInd in range(padX,N+padX):
				fImage[yInd,xInd] = sum(sum(padImg[yInd-padY:yInd+m-padY,xInd-padX:xInd+n-padX]*mask))

		return fImage[padY:-padY,padX:-padX]
