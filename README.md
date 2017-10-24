# Circle Hough Transform
Implementation of Hough Transform to detect Circles in an Image

[Circle Hough Transform](https://en.wikipedia.org/wiki/Circle_Hough_Transform) is a feature extraction technique used in Digital Image Processing to detect circles in an image. It is a specialized form of Hough Transform that utilizes three core techniques used in Image Processing - Image Filtering, Edge Detection and Hough Transform.

The project was implemented as a final project for the course _**CSE573: Computer Vision and Image Processing**_ at _University at Buffalo, The State University of New York_ during Fall 2016. The goal of the project is to detect circles in an image using Hough Transform.

### Implementation

Circle Hough Transform is implemented by "voting" in the Hough parameter space. The image is smoothened using a [Gaussian Filter](https://en.wikipedia.org/wiki/Gaussian_blur) to eliminate any unwanted noise. Then the edges are detected in the image using [Laplace of Gaussian](https://en.wikipedia.org/wiki/Blob_detection#The_Laplacian_of_Gaussian) with [Zero Crossing](https://en.wikipedia.org/wiki/Zero_crossing). This provides the basic outline in the image. At each point on the edge, voting for all possible circles is performed in the Hough space. The local maxima in the Hough space gives the circles. A threshold is used to identify qualifying local maxima's.

![Flowchart](https://github.com/PavanGJ/Circle-Hough-Transform/tree/master/res/Flow.png)

### Results

The implementation requires identifying optimal threshold values for edge detection and local maxima's. This is done iteratively by scanning through the threshold space.

![Input Image](https://github.com/PavanGJ/Circle-Hough-Transform/tree/master/res/HoughCircles.jpg)
![Hough Circle Detection](https://github.com/PavanGJ/Circle-Hough-Transform/tree/master/res/circles1.jpg)

We can see that Circle Hough Transform is able to detect even the occluded circles.
