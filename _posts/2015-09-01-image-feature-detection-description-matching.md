---
title: "Image Feature Detection, Description and Matching"
date: 2015-09-01T00:00:00-00:00
last_modified_at: 2015-09-01T00:00:00-00:00
categories:
  - computer vision
  - school project
permalink: /post-image-feature-detection-description-matching/
classes: wide
toc: True
excerpt: Discriminating and matching features in images.
header:
  og_image: /images/image-feature-detection-description-matching/0.webp
  teaser: /images/image-feature-detection-description-matching/0.webp
---

<figure class="half">
  <a href="/images/image-feature-detection-description-matching/0.webp">
    <img src="/images/image-feature-detection-description-matching/0.webp">
  </a>
  <a href="/images/image-feature-detection-description-matching/1.webp">
    <img src="/images/image-feature-detection-description-matching/1.webp">
  </a>
</figure>

<figure class="half">
  <a href="/images/image-feature-detection-description-matching/2.webp">
    <img src="/images/image-feature-detection-description-matching/2.webp">
  </a>
  <a href="/images/image-feature-detection-description-matching/3.webp">
    <img src="/images/image-feature-detection-description-matching/3.webp">
  </a>
</figure>

## Project Overview

The idea for this project was to detect discriminating features in an image and find the best matching features in other images. The detected features are invariant to basic transformations including translation, rotation, illumination and scale.

## Feature Detection

It can be rather difficult to describe qualitatively what makes a good feature worthy of detection in a computer vision project. One of the simplest methods is by corner detection. Most gray scale photos can be thought of as combination of uniform patches, lines and corners. Between those three features, the corner is by far the most detectable and unique. In a uniform patch, pixels adjacent to a single pixel do not vary much. In a line, the variation will only be in one direction. With a corner however, shifting the feature in any direction should pose a change in the intensity of the adjacent pixels. Selecting pixels that present the maximum change when shifted in any direction is the base of a very basic feature detection scheme.

To identify points of interest in the image, I will use the Harris corner detection method. That is to say, for each point in the image I consider a window of pixels around that point. I then compute the Harris matrix H for the point by summing the gradient of the pixel (as defined by a basic Sobel matrix) while including a weighting scheme defined by a gaussian filter. The weights of the gaussian filter were chosen to be circularly symmetric to account for rotation variance. To find interest points I define a corner strength function c(H) = determinant(H)/trace(H) and normalize by the global maximum in the photo. Once this corner strength value has been computed for every pixel, I choose points where c is above threshold and also where c is a local maximum among surrounding pixels.

### Computing Harris Features

```cpp
void ComputeHarrisFeatures(CFloatImage &image, FeatureSet &features)
{
	//Create grayscale image used for Harris detection
	CFloatImage grayImage=ConvertToGray(image);

	//Create image to store Harris values
	CFloatImage harrisImage(image.Shape().width,image.Shape().height,1);

	//Create image to store local maximum harris values as 1, other pixels 0
	CByteImage harrisMaxImage(image.Shape().width,image.Shape().height,1);

	
	//compute Harris values puts harris values at each pixel position in harrisImage. 
	//You'll need to implement this function.
	computeHarrisValues(grayImage, harrisImage);
	
	// Threshold the harris image and compute local maxima.  You'll need to implement this function.
	computeLocalMaxima(harrisImage,harrisMaxImage);
	// Prints out the harris image for debugging purposes
	CByteImage tmp(harrisImage.Shape());
	convertToByteImage(harrisImage, tmp);
	WriteFile(tmp, "harris.tga");
	
	//will then proceed to describe each feature... see feature descriptor
}
```

```cpp
/*Loop through the image to compute the harris corner values
srcImage:  grayscale of original image
harrisImage:  populate the harris values per pixel in this image*/
void computeHarrisValues(CFloatImage &srcImage, CFloatImage &harrisImage)
{
	//I think everything up to calculating c(H) will be done in this method
	//I think that the harrisImage is a 1 channel image (will appear as grayscale) and i will just populate that value with the c(H) value of that pixel
	int w = srcImage.Shape().width;
	int h = srcImage.Shape().height;



	//first compute Ix, Iy and the 2x2 matrix comprised of them
	CFloatImage gradientMatrices(srcImage.Shape().width, srcImage.Shape().height,4);
	computeGradientMatrices(srcImage, gradientMatrices);
	

	float c_H_max = 0;
	//for every pixel (not at the boarder)
	for (int y = 2; y < h - 2; y++) {
		for (int x = 2; x < w - 2; x++) {
			//use a nxn window around the pixel and multiply each 2x2 matrix from gradientMatrices for that pixel by the corresponding (by index) weight from the gaussian filter (nxn)
			//sum over all the 2 dimmensional matrices in that window
			float H_matrix[4] = { 0, 0, 0, 0 };
			
			//assume gaussian window is 5x5
			int startY = y - 2;
			int startX = x - 2;
			for (int i = startY; i < y + 3; i++){
				for (int j = startX; j < x + 3; j++){
					int matchingGaussianIndex = 5 * (i - y + 2) + (j - x + 2);
					H_matrix[0] += gradientMatrices.Pixel(j, i, 0)*gaussian5x5[matchingGaussianIndex];
					H_matrix[1] += gradientMatrices.Pixel(j, i, 1)*gaussian5x5[matchingGaussianIndex];
					H_matrix[2] += gradientMatrices.Pixel(j, i, 2)*gaussian5x5[matchingGaussianIndex];
					H_matrix[3] += gradientMatrices.Pixel(j, i, 3)*gaussian5x5[matchingGaussianIndex];				
				}
			}
						
			//calculate c(H) = det(H)/trace(H)
			float c_H = (H_matrix[0] * H_matrix[3] - H_matrix[2] * H_matrix[1]) / (H_matrix[0] + H_matrix[3]);
			harrisImage.Pixel(x, y, 0) = c_H;
			if (c_H > c_H_max){ //keep track of the maximum c_H to help normalize later
				c_H_max = c_H;
			}
		}
	}

	//normalize the intensity
	for (int y = 2; y < h - 2; y++) {
		for (int x = 2; x < w - 2; x++) {
			harrisImage.Pixel(x, y, 0) = harrisImage.Pixel(x, y, 0) / c_H_max;
		}
	}           
}
```

```cpp
/*computes Ix^2, IxIy; IyIx, Iy^2... the intermediate gradient matrix used in defining H*/
void computeGradientMatrices(CFloatImage &srcImage, CFloatImage &gradientMatrices)
{
	int w = srcImage.Shape().width;
	int h = srcImage.Shape().height;

	//for every pixel thats not on the boarders
	for (int y = 2; y < h-2; y++) {
		for (int x = 2; x < w-2; x++) {
			
			//for a box 5x5 centered around that pixel
			float Ix = 0;
			float Iy = 0;
			int startY = y - 2;
			int startX = x - 2;
			for (int i = startY; i < y + 3; i++){
				for (int j = startX; j < x + 3; j++){
					int matchingSobelIndex = 5 * (i - y + 2) + (j - x + 2);
					Ix += srcImage.Pixel(j, i, 0)*sobelX[matchingSobelIndex];
					Iy += srcImage.Pixel(j, i, 0)*sobelY[matchingSobelIndex];
				}
			}
			gradientMatrices.Pixel(x, y, 0) = Ix*Ix;
			gradientMatrices.Pixel(x, y, 1) = Ix*Iy;
			gradientMatrices.Pixel(x, y, 2) = Iy*Ix;
			gradientMatrices.Pixel(x, y, 3) = Iy*Iy;
		}
	}
}
```

### Computing Local Maxima

```cpp
/*Loop through the harrisImage to threshold and compute the local maxima in a neighborhood
srcImage:  image with Harris values
destImage: Assign 1 to a pixel if it is above a threshold and is the local maximum in 3x3 window, 0 otherwise.*/
void computeLocalMaxima(CFloatImage &srcImage, CByteImage &destImage)
{

	for (int y = 0; y < destImage.Shape().height; y++) {
		for (int x = 0; x < destImage.Shape().width; x++) {
			destImage.Pixel(x, y, 0) = 0;
		}
	}

	float strengthThreshold = 0.017;
	
	int w = srcImage.Shape().width;
	int h = srcImage.Shape().height;

	float currFeatureStrength = 0;
	float featureStrengthLocalMax = 0;
	float comparedPixelFeatureStrength = 0;

	
	/*by excluding features that are at pixels within 15pixels of the edges, we avoid boundary conditions 
	with the rotation 20x20 grid used in interpolation*/
	/*for every pixel (not within 15 pixels of the boarder)*/
	for (int y = 15; y < h - 15; y++) {
		for (int x = 15; x < w - 15; x++) {
			//check corner strength value of that pixel
			//if its above threshold, check to see if it is a local max in a 3x3 window
			currFeatureStrength = srcImage.Pixel(x, y, 0);
			if (currFeatureStrength >= strengthThreshold){
				//check that the pixel is a local maxima
				featureStrengthLocalMax = 0;

				for (int i = x - 1; i < x + 2; i++){
					for (int j = y - 1; j < y + 2; j++){
						//determine if pixel x,y is the local max in a 3x3 window
						if (i == x && j == y){
							//do nothing
						}
						else{
							comparedPixelFeatureStrength = srcImage.Pixel(i, j, 0);
							if (comparedPixelFeatureStrength > featureStrengthLocalMax){
								featureStrengthLocalMax = comparedPixelFeatureStrength;
							}
						}

					}
				}
				//if x,y is a local max, set that pixel to 1 and all other adjacent pixels default to 0
				if (currFeatureStrength > featureStrengthLocalMax){
					for (int i = x - 1; i < x + 2; i++){
						for (int j = y - 1; j < y + 2; j++){
							if (i == x && j == y){
								destImage.Pixel(x, y, 0) = 1;
							}
							else{
								destImage.Pixel(i, j, 0) = 0;
							}
						}
					}
					
					
				}

				//possible optimization (skip column if the feature is a local max)	
			}

		}
	}
}
```

### Performance

To demonstrate the operation of the original feature detector, two example images have been included with their resulting detected features. To discern the feature pixels, one might need to turn the brightness up on their display... as they can be hard to see.

<figure class="half">
<img src="/images/image-feature-detection-description-matching/0.webp">
<img src="/images/image-feature-detection-description-matching/1.webp">
</figure>

<figure class="half">
<img src="/images/image-feature-detection-description-matching/2.webp">
<img src="/images/image-feature-detection-description-matching/3.webp">
</figure>


## Feature Description (Using Image Pyramids)

After unique features have been detected/identified, it is necessary to describe these features thoroughly and efficiently so that a matching algorithm can easily compare the descriptions of two features from different images. A good feature descriptor must take into account changes in position, orientation and illumination.

### Overview + Major Design Choices

The general outline of my feature descriptor is the following:

- Define the Angle of Rotation for the feature.
- Use bilinear interpolation and the knowledge of the angle of rotation to create a new unrotated image from the original image (just a small space around the feature).
- Perform my own version of SIFT on the interpolated image.
- Normalize output vector from my SIFT, threshold the values and normalize the vector again.

```cpp
/*Loop through feature points in harrisMaxImage and create feature descriptor 
for each point above a threshold*/

int id = 0;
for (int y=0;y < harrisMaxImage.Shape().height;y++) {
	for (int x=0;x < harrisMaxImage.Shape().width;x++) {
	
		// Skip over non-maxima
		if (harrisMaxImage.Pixel(x, y, 0) == 0)
			continue;

		//else the pixel is a valid feature and needs some more description for future feature matching
		Feature f;
		f.id = id++;
		f.x = x;
		f.y = y;
		
		//f.type = ??;

		//Basic Process:
		//1. find the angle of rotation, store it in f.angleRadians
		//2. use bilinear interpolation to find a rotated 16x16 grid (that has been unrotated by the known angle of rotation)
		//3. perform sift on that new grid and store the 128element vector that describes the feature in f.data
			//when computing sift, make sure to not include features that are within 10 pixels of boarder to avoid a situation where the 16x16 grid or the 5x5 layered sobel on top extend beyond the boarder
		//4. store the feature


		//Process Step 1: 
		f.angleRadians = computeFeatureRotationAngle(grayImage, x, y);

		//Process Step 2:
		CFloatImage rotatedImage(20, 20, 1); //new image that will hold the un-rotated 16x16 grid (20x20 to account for sobel matrices)
		//assume the inner 16x16 grid to be centered around the pixel at 7,7
		interpolateRotatedImage(image, rotatedImage, f.x, f.y, f.angleRadians);

		//Process Step 3: 
		f.data = sift(rotatedImage);

		

		// Add the feature to the list of features
		features.push_back(f);
	}
}
```

### ​Defining the angle of rotation

The first step in describing each feature was to determine the angle of rotation from 0 radians (arbitrarily chosen to be +x pixel direction of the original image) to the eigenvector associated with the larger eigen value from that feature. Determining a descriptive angle using this method ensured that the same feature in a different image would be described the same way regardless of its default orientation.

```cpp
/*For the feature centered in srcImage, compute the angle of rotation based off 
	the eigenvector associated with the larger eigenvalue*/
float computeFeatureRotationAngle(CFloatImage &srcImage, int x, int y){
	
	int w = srcImage.Shape().width;
	int h = srcImage.Shape().height;

	float gradientMatrix[4]={ 0, 0, 0, 0 };
	float Ix = 0;
	float Iy = 0;
	int startY = y - 2;
	int startX = x - 2;
	//for every pixel thats not on the boarders
	//for a box 5x5 centered around that pixel
	for (int i = startY; i < y + 3; i++){
		for (int j = startX; j < x + 3; j++){
			int matchingSobelIndex = 5 * (i - y + 2) + (j - x + 2);
			Ix += srcImage.Pixel(j, i, 0)*sobelX[matchingSobelIndex];
			Iy += srcImage.Pixel(j, i, 0)*sobelY[matchingSobelIndex];
		}
	}
	gradientMatrix[0] = Ix*Ix;
	gradientMatrix[1] = Ix*Iy;
	gradientMatrix[2] = Iy*Ix;
	gradientMatrix[3] = Iy*Iy;
		

	float H_matrix[4] = { 0, 0, 0, 0 };

	//assume gaussian window is 5x5
	for (int i = startY; i < y + 3; i++){
		for (int j = startX; j < x + 3; j++){
			int matchingGaussianIndex = 5 * (i - y + 2) + (j - x + 2);
			H_matrix[0] += gradientMatrix[0]*gaussian5x5[matchingGaussianIndex];
			H_matrix[1] += gradientMatrix[1]*gaussian5x5[matchingGaussianIndex];
			H_matrix[2] += gradientMatrix[2]*gaussian5x5[matchingGaussianIndex];
			H_matrix[3] += gradientMatrix[3]*gaussian5x5[matchingGaussianIndex];
		}
	}

	float lambda_pos = 0.5*(H_matrix[0] + H_matrix[3] + sqrt(4 * H_matrix[1] * H_matrix[2] + (H_matrix[0] - H_matrix[3])*(H_matrix[0] - H_matrix[3])));
	//float lambda_neg = 0.5*(H_matrix[0] + H_matrix[3] - sqrt(4 * H_matrix[1] * H_matrix[2] + (H_matrix[0] - H_matrix[3])*(H_matrix[0] - H_matrix[3])));


	//solve for eigenvector components Vx and Vy associated with lambda_pos... 
	float V_x;
	float V_y;
	if (H_matrix[2] != 0){
		V_x = lambda_pos - H_matrix[3];
		V_y = H_matrix[2];
	}
	else if (H_matrix[1] !=0){
		V_x = H_matrix[1];
		V_y = lambda_pos - H_matrix[0];
	}
	else{
		V_x = 1;
		V_y = 0;
	}

	//return the angle of rotation calculated from that vector corresponding to the larger eigenvalue
	return atan2(V_y, V_x);

}
```

### Interpolating an un-rotated image

After the angle of rotation was calculated for each feature, it was possible to rotate that feature back around to 0 degrees. Feeding this result into the subsequent steps (SIFT) would ensure that the same features from different images would be described according to the same axis... therefore maintaining an invariance to rotation. In order to conduct this phase of the algorithm, a small window around the feature was taken from the original image and each pixel in that window was recalculated to be a new x and y coordinate after the counter rotation by the original angle found for that feature. This put the feature in a normalized orientation, but the x and y coordinates of the original pixels no longer fall on integer values associated with a pixel in the new counter rotated image. To create valuable pixels containing the same information as this counter-rotated image, each counter-rotated (x,y) coordinate was assigned an intensity value based off the 4 pixels around the location where it fell in the original image. To accomplish this, bilinear interpolation was used and the result was a normalized unrotated box containing the feature that could be fed into SIFT.

```cpp
/*conduct bilinear interpolation to find a rotated 16x16 grid(that has been unrotated by the known angle of rotation)*/
void interpolateRotatedImage(CFloatImage &srcImage, CFloatImage rotatedImage, int pX, int pY, float angle){

	//pX,pY is assumed to be indice 7,7 in the 16x16 grid. Therefore in the 20x20 grid it is actually indices 9,9
	//the top left corner of the 20x20 block is therefore at coordinate (pX-9, pY-9) in the srcImage
	//the bottom right corner of the 20x20 block is therefore at coordinate (pX+10,pY+10)

	float x_rot, y_rot, A, B, C, D, interpolatedIntensity;
	int x0, x1, y0, y1;
	//for every pixel in srcImage in a 20x20 box around the feature point pX,pY... interpolate a new rotated value to be placed in rotatedImage
	for (int x = pX - 9; x < pX + 11; x++){
		for (int y = pY - 9; y < pY + 11; y++){

			x_rot = (x - pX)*cos(angle) - (y - pY)*sin(angle) + pX;
			y_rot = (x - pX)*sin(angle) + (y - pY)*cos(angle) + pY;

			// check and handle rotations where the x' and y' are ints... and where one of them is but the other is not
			if (floorf(x_rot) == x_rot && floorf(y_rot) == y_rot){
				//if both of the rotated coordinates are ints
				//(ie: they fall on exact pixels and the rotationw was a multiple of 90 degrees)
				//simply weight that pixel value by 100% for the inteprolation... ie no need to interpolate
				rotatedImage.Pixel(x - (pX - 9), y - (pY - 9), 0) = srcImage.Pixel(int(x_rot), int(y_rot), 0);
			}
			else if (floor(x_rot) == x_rot){
				//if the x coordinate falls on an int... interpolate between the pixel above and below the coordinate

				y0 = int(y_rot);
				y1 = y0 + 1;

				//calculate the length of the lines formed by the coordiante and the 2 adjacent pixels on the same col
				A = (y_rot - y0);
				B = (y1 - y_rot);
				interpolatedIntensity = srcImage.Pixel(x_rot, y0, 0) * B
					+ srcImage.Pixel(x_rot, y1, 0)*A;

				rotatedImage.Pixel(x - (pX - 9), y - (pY - 9), 0) = interpolatedIntensity;

			}
			else if (floor(y_rot) == y_rot){
				//if the y coordinate falls on an int... interpolate between the pixel to the left and to the right

				x0 = int(x_rot);
				x1 = x0 + 1;

				//calculate the length of the lines formed by the coordiante and the 2 adjacent pixels on the same row
				A = (x_rot - x0);
				B = (x1 - x_rot);
				interpolatedIntensity = srcImage.Pixel(x0, y_rot, 0) * B
					+ srcImage.Pixel(x1, y_rot, 0)*A;

				rotatedImage.Pixel(x - (pX - 9), y - (pY - 9), 0) = interpolatedIntensity;

			}
			else{
				//the coordinate is not an integer in either dimension, so perform bilinear interpolation

				x0 = int(x_rot);
				x1 = x0 + 1;
				y0 = int(y_rot);
				y1 = y0 + 1;
				//calculate the areas of the rectangles formed by the rotated coordinate and its 4 closest pixels
				A = (x_rot - x0)*(y_rot - y0);
				B = (x1 - x_rot)*(y_rot - y0);
				C = (x_rot - x0)*(y1 - y_rot);
				D = (x1 - x_rot)*(y1 - y_rot);

				interpolatedIntensity = srcImage.Pixel(x0, y0, 0) * D
					+ srcImage.Pixel(x1, y0, 0) * C
					+ srcImage.Pixel(x0, y1, 0) * B
					+ srcImage.Pixel(x1, y1, 0) * A;

				rotatedImage.Pixel(x - (pX - 9), y - (pY - 9), 0) = interpolatedIntensity;
			}
		}
	}

}
```

### SIFT

To further describe the feature, I chose to implement a version of the SIFT algorithm because of its powerful nature and simplicity. My algorithm splits the angle normalized image containing the feature into 16 small 4x4 pixel boxes. For each box the gradient of each pixel is calculated. Then the magnitude of that gradient vector is added to one of 8 buckets that each represent 1/8th of the 2*pi range on a complete circle. The angle of the gradient vector determines which bucket the vector's magnitude will be added to. This is a very simple histogram. Once each of the 16 4x4 boxes has a completed 8 element vector, all 16 of the 8 element vectors are collectively stored in a single 128 element vector.

```cpp
/*conduct the sift procedure on the 16x16 grid centered in the 20x20 srcImage*/
vector sift(CFloatImage &srcImage){
	//first calculate the gradient Ix and Iy  (dI/dx and dI/dy) at every pixel in the image
	//only the Ix and Iy components will be necessary, but I'll just take what i need from gradientMatrices after its all calculated
	CFloatImage gradientMatrices(srcImage.Shape().width, srcImage.Shape().height, 4);
	computeGradientMatrices(srcImage, gradientMatrices);

	//initialize a vector to hold the 128 element description that will be returned
	vector siftResult(128);


	//initialize a vector of empty buckets that will be cleared and re-used for every 4x4 block
	//the first element holds the combined magnitude of gradients in the 0 -> 2*pi/8 range...
	//the second element holds the combined magnitude of gradients in the 2*pi/8 -> 2(2*pi/8) range 
	//etc..
	float buckets[8] = { 0, 0, 0, 0, 0, 0, 0, 0 };
	
	// partial derivatives of intensity, ie: vector components of the gradient
	float Ix = 0;
	float Iy = 0;


	//divide the 16x16 grid centered in the 20x20 srcImage into 16 different 4x4 blocks
	for (int row = 0; row < 4; row++){
		for (int col = 0; col < 4; col++){
			
			//reset the buckets to 0
			for (int bucketIdx = 0; bucketIdx < 8; bucketIdx++){
				buckets[bucketIdx] = 0;
			}

			//for each 4x4 block, calculate the 8 bucket (histogram) vector describing its gradient
			//upper left corner of the current 4x4 block is at pixel (2+row*4, 2+col*4)
			for (int i = 0; i < 4; i++){
				for (int j = 0; j < 4; j++){
					//current coordinate in the 4x4 box is i,j... 
					//current coordiante in the 16x16 box is col*4+i, row*4+j... 
					//current coordinate in the 20x20 box is 2+col*4+i, 2+row*4+j...
					
					//the value of Ix and Iy gradient components are calculated below
					Ix = sqrt(gradientMatrices.Pixel(2 + col * 4 + i, 2 + row * 4 + j, 0));
					Iy = sqrt(gradientMatrices.Pixel(2 + col * 4 + i, 2 + row * 4 + j, 3));
					
					//FIXME: don't know if this will be right because the y axis faces downward in the image??? but im treating it as if it is upwards??
					//in the end the descriptor should be consistent between different images that use it... so it shouldn't matter
					float vectorMagnitude = sqrt(Ix*Ix+Iy*Iy); //the magnitude of the combinant vector
					float vectorRadianAngle = atan2(Iy, Ix);  //an angle describing the combinant vector in radians (returns value between -pi and pi)
					
					if (vectorRadianAngle < 0){
						vectorRadianAngle += 2 * PI;
					}
					//sum the magnitudes in their corresponding buckets
					buckets[int(vectorRadianAngle / (2 * PI / 8))] += vectorMagnitude;

				}
			}
			
			//place the bucket values in the final 128 element vector in the correct place.
			for (int k = 0; k < 8; k++){
				siftResult[row * 32 + col * 8 + k] = buckets[k];
			}
			
		}
	}
	return siftResult;
}
```

### Normalizing output vector

At the end of my SIFT algorithm, I normalize the 128 element vector to unit length to maintain in-variance to changes in illumination. I also proceeded to threshold the normalized values to a value of 0.2 and then re-normalize the vector a second time. This helped maintain in-variance to non-linear changes in illumination.
​
Without this normalization technique the AUC for bench-marking the bikes image set was 0.687217 whereas with the normalization the AUC was 0.694351. This image set didn't have very drastic changes in illumination however. Looking at leuven image set, where illumination change is more apparent, the AUC jumped from 0.758304 to 0.832059 when I included the normalization. This is a much larger change and demonstrates how image sets with variation in illumination are handled with the inclusion of my normalization technique. My technique appears to be very effective.

```cpp
//normalize the vector to unit length in order to enhance invariance to illumination
float length_squared = 0;
for (int k = 0; k < 128; k++){
	length_squared += siftResult[k]*siftResult[k];
}
float length = sqrt(length_squared);
bool normalizeAgain = false;
for (int k = 0; k < 128; k++){
	siftResult[k] = siftResult[k] / length;
	if (siftResult[k]>0.2){
		siftResult[k] = 0.2;
		normalizeAgain = true;
	}
}

//reduce effects of non-linear illumination by using a threshold of 0.2 and normalizing again
if (normalizeAgain){
	float length_squared = 0;
	for (int k = 0; k < 128; k++){
		length_squared += siftResult[k] * siftResult[k];
	}
	float length = sqrt(length_squared);

	for (int k = 0; k < 128; k++){
		siftResult[k] = siftResult[k] / length;
		if (siftResult[k]>0.2){
			siftResult[k] = 0.2;
		}
	}
}
```

### Performance (ROC curves)

The following curves and tables describe the performance of the matching using my implementation of a descriptor compared to some of the leading SIFT implementations available today. Additionally they compare the use of a simple sum of squares difference when matching and a ratio test for matching. See my feature matching page to view the code for these two matching types.

ROC curve for the graf photos (AUC values in the table).

My Implementation + SSD|My Implementation + Ratio|SIFT + SSD|SIFT + Ratio
:--------:|:--------:|:--------:|:--------:
0.782022|0.774843|0.932023|0.966663

![results1](/images/image-feature-detection-description-matching/4.webp){:.align-center}

ROC curve for the yosemite photos (AUC values in the table)

My Implementation + SSD|My Implementation + Ratio|SIFT + SSD|SIFT + Ratio
:--------:|:--------:|:--------:|:--------:
0.885658|0.890320|0.994692|0.993979

![results2](/images/image-feature-detection-description-matching/5.webp){:.align-center}

### Performance (Average AUC)

​My Own Descriptor and Ratio Test Matching

Bikes|Graf|Leuven|Wall|Average
:--------:|:--------:|:--------:|:--------:|:--------:
0.694351|0.610892|0.832059|0.718335|0.713909

​My Own Descriptor and SSD Test Matching

Bikes|Graf|Leuven|Wall|Average
:--------:|:--------:|:--------:|:--------:|:--------:
0.654525|0.611547|0.857094|0.736532|0.714925

### Strengths and Weaknesses of Algorithm

My chosen implementation is particularly resilient to changes in illumination, translation and rotation, but not to changes in scale (at least not by design). The SIFT method should be slightly invariant to scale intrinsically, but I did not pursue the inclusion of Gaussian image pyramids to specifically target scale changes. My performance scores indicate the best performance was on images with variance in translation (bikes) and illumination (leuven). Quantitatively, these were the best results. I also cut off the outermost 15 pixels around the whole border to avoid edge case conditions which may have impacted the performance.

## Feature Matching

Once the noteworthy features in an image have been described, it is trivial to compare the descriptions to features from other images and define a match strength between features in the photos.

```cpp
// This just uses the ratio of the SSD distance of the two best matches as the score
// and matches a feature in the first image with the closest feature in the second image.
// It can match multiple features in the first image to the same feature in
// the second image.
void ratioMatchFeatures(const FeatureSet &f1, const FeatureSet &f2, vector &matches, double &totalScore)
{
	int m = f1.size();
	int n = f2.size();

	matches.resize(m);
	totalScore = 0;

	double d;
	double dBest;
	double dSecondBest;
	int idBest;

	for (int i = 0; i < m; i++)
	{
		dBest = 1e100;
		idBest = 0;

		for (int j = 0; j < n; j++)
		{
			d = distanceSSD(f1[i].data, f2[j].data);

			if (d < dBest)
			{
				dSecondBest = dBest;
				dBest = d;
				idBest = f2[j].id;
			}
		}

		matches[i].id1 = f1[i].id;
		matches[i].id2 = idBest;
		matches[i].score = dBest / dSecondBest;
		totalScore += matches[i].score;
	}
}
```

```cpp
// Perform simple feature matching.  This just uses the SSD
// distance between two feature vectors, and matches a feature in the
// first image with the closest feature in the second image.  It can
// match multiple features in the first image to the same feature in
// the second image.
void ssdMatchFeatures(const FeatureSet &f1, const FeatureSet &f2, vector &matches, double &totalScore)
{
	int m = f1.size();
	int n = f2.size();

	matches.resize(m);
	totalScore = 0;

	double d;
	double dBest;
	int idBest;

	for (int i = 0; i < m; i++)
	{
		dBest = 1e100;
		idBest = 0;

		for (int j = 0; j < n; j++)
		{
			d = distanceSSD(f1[i].data, f2[j].data);

			if (d < dBest)
			{
				dBest = d;
				idBest = f2[j].id;
			}
		}

		matches[i].id1 = f1[i].id;
		matches[i].id2 = idBest;
		matches[i].score = dBest;
		totalScore += matches[i].score;
	}
}
```
