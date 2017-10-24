from impy import imarray
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import imread

def smoothen(img,display):
    #Using a 3x3 gaussian filter to smoothen the image
    gaussian = np.array([[1/16.,1/8.,1/16.],[1/8.,1/4.,1/8.],[1/16.,1/8.,1/16.]])
    img.load(img.convolve(gaussian))
    if display:
        img.disp
    return img

def edge(img,threshold,display=False):
    #Using a 3x3 Laplacian of Gaussian filter along with sobel to detect the edges
    laplacian = np.array([[1,1,1],[1,-8,1],[1,1,1]])
    #Sobel operator (Orientation = vertical)
    sobel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

    #Generating sobel horizontal edge gradients
    G_x = img.convolve(sobel)

    #Generating sobel vertical edge gradients
    G_y = img.convolve(np.fliplr(sobel).transpose())

    #Computing the gradient magnitude
    G = pow((G_x*G_x + G_y*G_y),0.5)

    G[G<threshold] = 0
    L = img.convolve(laplacian)
    if L is None:                                                               #Checking if the laplacian mask was convolved
        return
    (M,N) = L.shape

    temp = np.zeros((M+2,N+2))                                                  #Initializing a temporary image along with padding
    temp[1:-1,1:-1] = L                                                         #result hold the laplacian convolved image
    result = np.zeros((M,N))                                                    #Initializing a resultant image along with padding
    for i in range(1,M+1):
        for j in range(1,N+1):
            if temp[i,j]<0:                                                     #Looking for a negative pixel and checking its 8 neighbors
                for x,y in (-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1):
                        if temp[i+x,j+y]>0:
                            result[i-1,j-1] = 1                                 #If there is a change in the sign, it is a zero crossing
    img.load(np.array(np.logical_and(result,G),dtype=np.uint8))
    if display:
        img.disp
    return img

def detectCircles(img,threshold,region,radius = None):
    (M,N) = img.shape
    if radius == None:
        R_max = np.max((M,N))
        R_min = 3
    else:
        [R_max,R_min] = radius

    R = R_max - R_min
    #Initializing accumulator array.
    #Accumulator array is a 3 dimensional array with the dimensions representing
    #the radius, X coordinate and Y coordinate resectively.
    #Also appending a padding of 2 times R_max to overcome the problems of overflow
    A = np.zeros((R_max,M+2*R_max,N+2*R_max))
    B = np.zeros((R_max,M+2*R_max,N+2*R_max))

    #Precomputing all angles to increase the speed of the algorithm
    theta = np.arange(0,360)*np.pi/180
    edges = np.argwhere(img[:,:])                                               #Extracting all edge coordinates
    for val in range(R):
        r = R_min+val
        #Creating a Circle Blueprint
        bprint = np.zeros((2*(r+1),2*(r+1)))
        (m,n) = (r+1,r+1)                                                       #Finding out the center of the blueprint
        for angle in theta:
            x = int(np.round(r*np.cos(angle)))
            y = int(np.round(r*np.sin(angle)))
            bprint[m+x,n+y] = 1
        constant = np.argwhere(bprint).shape[0]
        for x,y in edges:                                                       #For each edge coordinates
            #Centering the blueprint circle over the edges
            #and updating the accumulator array
            X = [x-m+R_max,x+m+R_max]                                           #Computing the extreme X values
            Y= [y-n+R_max,y+n+R_max]                                            #Computing the extreme Y values
            A[r,X[0]:X[1],Y[0]:Y[1]] += bprint
        A[r][A[r]<threshold*constant/r] = 0

    for r,x,y in np.argwhere(A):
        temp = A[r-region:r+region,x-region:x+region,y-region:y+region]
        try:
            p,a,b = np.unravel_index(np.argmax(temp),temp.shape)
        except:
            continue
        B[r+(p-region),x+(a-region),y+(b-region)] = 1

    return B[:,R_max:-R_max,R_max:-R_max]

def displayCircles(A):
    img = imread(file_path)
    fig = plt.figure()
    plt.imshow(img)
    circleCoordinates = np.argwhere(A)                                          #Extracting the circle information
    circle = []
    for r,x,y in circleCoordinates:
        circle.append(plt.Circle((y,x),r,color=(1,0,0),fill=False))
        fig.add_subplot(111).add_artist(circle[-1])
    plt.show()

file_path = './res/HoughCircles.jpg'
img = imarray(file_path)
res = smoothen(img,display=False)                                               #set display to True to display the edge image
res = edge(res,128,display=False)                                               #set display to True to display the edge image
#detectCircles takes a total of 4 parameters. 3 are required.
#The first one is the edge image. Second is the thresholding value and the third is the region size to detect peaks.
#The fourth is the radius range.
res = detectCircles(res,8.1,15,radius=[100,10])
displayCircles(res)
