---
title: "Facial Detection & Recognition"
date: 2015-11-01T00:00:00-00:00
last_modified_at: 2015-11-01T00:00:00-00:00
categories:
  - computer vision
  - school project
permalink: /post-facial-detection-and-recognition/
classes: wide
toc: True
excerpt: Creating 360 panoramas from a set of images.
header:
  og_image: /images/facial-detection-and-recognition/0.webp
  teaser: /images/facial-detection-and-recognition/0.webp
---

![preview](/images/facial-detection-and-recognition/0.webp){:.align-center}

## Overview + Major Design Choices

Data points can exist as coordinates in space of infinite dimensions. Faces however, as varied as they may be, tend to congregate in a similar subspace of that infinitely dimensional space. By defining that subspace as a hyperplane spanned by k vectors (an idea easier to grasp when reducing 3 dimensions to 2, but equally valid for larger dimension quantities), then a point on the hyperplane can be represented using only k coefficients. The general process is as described below:

- Take a representative sample of data points and find the subspace with the desired dimensionality that best fits the sample data.
- With that stored subspace, one can easily check if a new point is a valid data point by projecting it onto the subspace and measuring the error difference between the point and its projection.
- Represent each face image as a vector of pixel values. To do this, train the face recognition algorithm with some input faces, then crop and scale the desired face image and normalize its intensity before recognizing it with a trained algorithm.

## Using PCA to generate Eigenfaces from set of User Faces

The following method contents calculate the average face and then use the difference from that average face to determine the eigen values and vectors of an A matrix. The vectors are sorted and the best are placed in result.

```cpp
// size the results vector
results.resize(n);
results.setHeight(height);
results.setWidth(width);


/***************BEGIN PARAMETERS****************/

//Vector Size
int vector_size = height*width;
//Average Face 
Face avgFace = Face(width, height);
// Compute number of images in the database
int numImages = (*this).getSize();
//Difference from the average face
Face diffFromAvg = Face(width, height);

/*Holds the A Matrix*/
double** A_Matrix = Jacobi::matrix(1, vector_size, 1, vector_size);
/* Holds the Eigen Values*/
double* eigenvec = Jacobi::vector(1, vector_size);
/* Holds the Eigen Vectors*/
double** eigmatrix = Jacobi::matrix(1, vector_size, 1, vector_size);
/*Number of Rotations*/
int* nrot = new int();
/*Will hold the result of successive dot product calls*/
Array dP_Result;
dP_Result.resize(vector_size);
/*Will hold the ordered eigen vectr indices*/
Array orderedEigenVecs;
/**************END PARAMETERS****************/



//First actually calculate the average face
for (int i = 0; i < width; i++){
	for (int j = 0; j < height; j++){
		for (int eigIndex = 0; eigIndex < numImages; eigIndex++){
			avgFace.pixel(i, j, 0) += (*this)[eigIndex].pixel(i, j, 0);
		}
	}
} 

//Noramlize the average face
avgFace /= numImages;
results.setAverage(avgFace);


/*Calculate the Eigen Vectors*/

/*Set all the matrices and vectors to 0*/
for (int i = 1; i <= vector_size; i++){
	for (int j = 1; j <= vector_size; j++){
		A_Matrix[i][j] = 0.0;
		eigmatrix[i][j] = 0.0;
	}
	eigenvec[i] = 0.0;
}

/*Compute A and A*AT*/
for (int i = 0; i < numImages; i++){
	// Subtract this image from the average fface and store in the difference
	(*this)[i].sub(avgFace, diffFromAvg);
	
	for (int x = 0; x < width; x++){
		for (int y = 0; y < height; y++){
			dP_Result[x + y*width] = diffFromAvg.pixel(x, y, 0);
		}
	}

	/* Compute A*AT */
	for (int j = 0; j < vector_size; j++){
		for (int k = 0; k < vector_size; k++){
			A_Matrix[j + 1][k + 1] += dP_Result[j] * dP_Result[k];
		}
	}
}


/*Calculate Eigen Vectors of the A Matrix*/
Jacobi::jacobi(A_Matrix, vector_size, eigenvec, eigmatrix, nrot);

//Sort the EigenVectors 
sortEigenvalues(eigenvec, orderedEigenVecs);
//Place the best n results in results
for (int rCount = 0; rCount < n; rCount++){
	int eigVecIndex = orderedEigenVecs[rCount] + 1;
	for (int x = 0; x < width; x++){
		for (int y = 0; y < height; y++){
			results[rCount].pixel(x, y, 0) = eigmatrix[x+ y*width + 1][eigVecIndex];
		}
	}
}

/* Free any used Allocated Space */
Jacobi::free_matrix(A_Matrix, 1, vector_size, 1, vector_size);
Jacobi::free_matrix(eigmatrix, 1, vector_size, 1, vector_size);
Jacobi::free_vector(eigenvec, 1, vector_size);	
```

## Projecting Faces

This method is simple, it calculates the difference between the average face and the current face and then uses the dotproduct to calcualte the projection.

```cpp
//u will hold the difference between the avgFace(mu) and the current face
Face u = Face(width, height);
//actually compute the difference u by subtracting the avg from the face
face.sub(average_face, u);

//projection is just a dotproduct
for (int i = 0; i < getSize(); i++){
	coefficients[i] = u.dot((*this)[i]);
}	
```

## Construct Face

This method accumulates the construct.

```cpp
int k = coefficients.getSize();
Face accumulator = average_face;
Face placeHolder = Face((*this).average_face.getWidth(), (*this).average_face.getHeight());
for (int i = 0; i < k; i++){
	placeHolder = (*this)[i];
	placeHolder *= coefficients[i];
	accumulator.add(placeHolder, accumulator);
}
result = accumulator;
```

## ​Face Detection

isFace determines the coefficients of an input face, then compares the construct from those coefficients to see if the constructed face is a valid face by a permittable mse score.

```cpp
//create a new vector to hold the coefficients
Vector coefficients;

//then project the face to determine the coefficients
projectFace(face, coefficients);

//create  blank test face to receive a constructed face from the coeffcicients
Face testFace;
//then construct the face
constructFace(coefficients, testFace);

//store the the mean square error between face and testFace in "mse"
mse = face.mse(testFace);

//return a boolean of whether or not the mse was less than threshold, to indicate if "face" is indeed a face
if (mse <= max_reconstructed_mse){
	return true;
}
else{
	return false;
}
```

## Face Verification

Time can be saved during face verification by comparing the coefficients directly instead of constructing a new face. Otherwise it is very similar to the previous method.

```cpp
/*Alternatively, could have done the following to avoid a construction*/

Vector coefficients;
projectFace(face, coefficients);
mse = user_coefficients.mse(coefficients);

/*return a boolean of whether or not the mse was less than threshold, this
indicates if the given face acceptably matched a construction of the users face */
if (mse < max_coefficients_mse){
	return true;
}
else{
	return false;
}
```

## Face Recognition

Recognize face simply goes through the list of users and determines the quality of the match for each, then sorts it.

```cpp
// Get the coefficients for this face in eigenface space
Vector coefficients;
projectFace(face, coefficients);

//iterate through users and set the mse for each
for (int i = 0; i < users.getSize(); i++){
	users[i].setMse(users[i].mse(coefficients));
}
//then sort the list "users"
users.sort();
```

## Finding Faces

This method finds the best n faces that don't overlap eachother. It iterates through the pixels different rescaled versions of the image to determine if a face exists. It keeps a running list of the found faces and replaces them when it finds better versions of the same face at a different scale or a different pixel start location. Then depending on input arguments, the method crops or outlines the faces.

```cpp
/* things needed later*/
Image scaledImg; //will hold the scaled versions of the image

Vector coefficients;
coefficients.resize((*this).getSize());
double face_threshold = 1;

Face tempFace;
Face tempFaceBlank;

double curr_mse;
int facesSeen = 0;

int faceBoxHalfHeight = 15;
int faceBoxHalfWidth = 13;


/*
eigfaces.h has a FacePosition structure that will be useful, it takes the following...
int x,y
double scale
double error
*/
FacePosition fpos;
fpos.error = 100000; //make sure that if something is a face it will replace the dummy 1st item put in this list.

//create a list of face positions, and place the first undefined one in it.
std::list fpos_list;
fpos_list.push_front(fpos);

//can i set these once out here, or do they change... i don't believe they do.
int img_w = img.getWidth();
int img_h = img.getHeight();
int w, h;


double curr_scale;
/* keep track of the current scale being used and start it at the min_scale*/
for (curr_scale = min_scale; curr_scale <= max_scale; curr_scale += step){
	printf("Changing scale to %f\n", curr_scale);


	// Determine the dimensions of the scaled image based off the current scale
	w = (int)(img_w*curr_scale);
	h = (int)(img_h*curr_scale);
	//then effectively scale the image
	scaledImg.resize(w, h);
	img.resample(scaledImg);

	//for every pixel in the image, see if a face begins there
	// discouint pixels that are within half a facebox width or height of the edges
	for (int x = faceBoxHalfWidth; x < w - faceBoxHalfWidth; x++){
		for (int y = faceBoxHalfHeight; y < h - faceBoxHalfHeight; y++){

			//set temp face to match the right size
			tempFace.resize((*this).getWidth(), (*this).getHeight());
			//set temp face to be a normalized grayscale image
			tempFace.subimage(x, x + (*this).getWidth() - 1, y, y + (*this).getHeight() - 1, scaledImg, false);

			//calculate the mse of this first loose pass, storing it in curr_mse
			bool firstTestPositive = isFace(tempFace, 800, curr_mse);

			//if the mse was acceptable, then check it further
			if (firstTestPositive){
				fpos.x = x;
				fpos.y = y;
				fpos.scale = curr_scale;
				fpos.error = curr_mse;

				/*check if the current face at fpos has already been found*/

				//define some parameters to help in the check
				double x_tooClose = (double)(*this).getWidth() / 2.0;
				double y_tooClose = (double)(*this).getHeight() / 2.0;
				double unscaled_x_curr = (double) 1.0*fpos.x / fpos.scale;
				double unscaled_y_curr = (double) 1.0*fpos.y / fpos.scale;
				double unscaled_x_compare, unscaled_y_compare, diff_x, diff_y;

				bool foundOverlap = false;
				//iterate through the list of known face positions


				std::list::iterator iterator;
				for (iterator = fpos_list.begin(); iterator != fpos_list.end(); ++iterator) {
					//define more parameters
					unscaled_x_compare = (double)(*iterator).x / (*iterator).scale;
					unscaled_y_compare = (double)(*iterator).y / (*iterator).scale;
					diff_x = abs(unscaled_x_compare - unscaled_x_curr);
					diff_y = abs(unscaled_y_compare - unscaled_y_curr);

					//check that the current face in question isn't too close to an existing find in the list
					if (diff_x < x_tooClose && diff_y < y_tooClose && (*iterator).x != -1){
						/*The images are too close together...
						1. assume the images represent the same face
						2. check to see which image has the better error value (mse)
						3. discard the worse image, and keep the better one*/

						/*Case 1: newly found image is the better one, so replace the image in the list and resort the list*/
						if ((*iterator).error >= fpos.error){

							(*iterator) = fpos;
							fpos_list.sort(myComparatorFunction);
							printf("Replacing Face with better version.\n");
						}
						foundOverlap = true;
						break;
					}
				}

				if (!foundOverlap){
					fpos_list.push_front(fpos);
					fpos_list.sort(myComparatorFunction);
					printf("Found a new face... added it to the list and resorted\n");
					break; //FIXME: should this break be here?
				}

			}//end of the firstTestPositive case
		
		}
	}//end of the loop through every pixel in the image


}//end of the scale changes loop

printf("Finished finding faces. Total of %i faces found.\n", fpos_list.size());
std::list::iterator iterator;
if (!fpos_list.empty()){
	for (iterator = fpos_list.begin(); iterator != fpos_list.end(); ++iterator) {
		printf("face(%d,%d), mse=%f\n", (int)((*iterator).x / (*iterator).scale), (int)((*iterator).y / (*iterator).scale), (*iterator).error);
	}
}



if (crop == true){
	if (fpos_list.empty()){
		printf("no faces found to crop in the image\n");
	}
	else{
		printf("entering crop phase\n");
		FacePosition f = fpos_list.front();
		printf("f.x is %i, f.y is %i, and f.scale is %f \n", f.x, f.y, f.scale);
		int x_min_unscaled = (int)f.x / f.scale; //xmin (left side of the image)
		int y_min_unscaled = (int)f.y / f.scale; //ymin 
		//use the average face to get the max width of a cropped face, add it to f.x to get right side
		int x_max = (int)f.x + (*this).average_face.getWidth(); 
		int x_max_unscaled = (int)x_max / f.scale;
		//use the average face to get the max height of a cropped face
		int y_max = (int)f.y + (*this).average_face.getHeight(); 
		int y_max_unscaled = (int)y_max / f.scale;
		printf("the corners are at: %i, %i, %i, %i", x_min_unscaled, y_min_unscaled, x_max_unscaled, y_max_unscaled);

		img.crop(x_min_unscaled, y_min_unscaled, x_max_unscaled, y_max_unscaled, result);
	}

}
else{
	printf("entering mark phase\n");
	//replicate the entire image but with green lines around the faces
	result.resize(img.getWidth(), img.getHeight(), img.getColors());
	img.resample(result);
	int x0, x1, y0, y1;

	//only want to outline the first n faces, so keep track of how many have been outlined
	int drawCount = 0;
	//get the position of every face in the list using iterator
	std::list::iterator iterator;
	for (iterator = fpos_list.begin(); iterator != fpos_list.end(); ++iterator) {
		if (drawCount >= n){
			break;
		}
		drawCount++;
		//calculate the corners of the box around the face held at position in Iterator
		x0 = (int)(*iterator).x / (*iterator).scale;
		x1 = (int)((*iterator).x + (*this).average_face.getWidth()) / (*iterator).scale;
		y0 = (int)(*iterator).y / (*iterator).scale;
		y1 = (int)((*iterator).y + (*this).average_face.getHeight()) / (*iterator).scale;

		//draw lines around the face
		result.line(x0, y1, x1, y1, 100, 255, 100);
		result.line(x1, y0, x1, y1, 100, 255, 100);
		result.line(x0, y0, x0, y1, 100, 255, 100);
		result.line(x0, y0, x1, y0, 100, 255, 100);
	}
}
```

## Testing Recognition with Reference Images

### Computing 10 eigenfaces from cropped neutral face students

Average Face | Eigen Face 0 | Eigen Face 1 | Eigen Face 2 |Eigen Face 3 | Eigen Face 4 | Eigen Face 5 | Eigen Face 6 | Eigen Face 7 | Eigen Face 8 | Eigen Face 9
:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:|:--------:
[![placeholder](/images/facial-detection-and-recognition/1.webp){:.align-enter}](/images/facial-detection-and-recognition/1.webp) |[![placeholder](/images/facial-detection-and-recognition/2.webp){:.align-enter}](/images/facial-detection-and-recognition/2.webp) |[![placeholder](/images/facial-detection-and-recognition/3.webp){:.align-enter}](/images/facial-detection-and-recognition/3.webp) |[![placeholder](/images/facial-detection-and-recognition/4.webp){:.align-enter}](/images/facial-detection-and-recognition/4.webp) |[![placeholder](/images/facial-detection-and-recognition/5.webp){:.align-enter}](/images/facial-detection-and-recognition/5.webp) |[![placeholder](/images/facial-detection-and-recognition/6.webp){:.align-enter}](/images/facial-detection-and-recognition/6.webp) |[![placeholder](/images/facial-detection-and-recognition/7.webp){:.align-enter}](/images/facial-detection-and-recognition/7.webp) |[![placeholder](/images/facial-detection-and-recognition/8.webp){:.align-enter}](/images/facial-detection-and-recognition/8.webp) |[![placeholder](/images/facial-detection-and-recognition/9.webp){:.align-enter}](/images/facial-detection-and-recognition/9.webp) |[![placeholder](/images/facial-detection-and-recognition/10.webp){:.align-enter}](/images/facial-detection-and-recognition/10.webp) |[![placeholder](/images/facial-detection-and-recognition/11.webp){:.align-enter}](/images/facial-detection-and-recognition/11.webp)

### Experimenting with the Number of Eigenfaces Used

The procedure above was computed for the following # of eigenfaces: 1,3,5,7,9,10,11,13,15,17,19,21,23. For each set of images a user base was computed and the program was run to recognize the photos from a reference set of faces with interesting facial expressions. The accuracy of facial recognition (to the resting face of the correct match) was computed and the results were found below. It seemed that the number of eigenfaces used dictated the accuracy up until a point where it plateaued. 15 eigenfaces seemed to be the general tipping point for this data set. I imagine that the subtle ups and downs after the plateau are due to the data set reacting one way or the other because of its small size. In general I would expect more eigen faces to produce better results, but after a certain point the marginal benefit of what another vector can convey isn't worth the processing power. Further eigenfaces won't greatly affect accuracy. I used 15 eigenfaces for the subsequent experiments. It seemed from the noted errors that certain interesting images 16, 15, 7, 4 and 2 produced the most errors. Almost all these photos were people with glasses. I suspect this is the reason for their error in detection.

<figure class="half">
    <img src="/images/facial-detection-and-recognition/12.webp">
    <img src="/images/facial-detection-and-recognition/13.webp">
</figure>

## Finding and Marking Faces in Group Photos

Almost all the group photos worked really well for finding faces. I show groups the following two groups below because they are examples of both a good and a bad match. I believe the mistake shown is due to the facial hair on the individual on the left. Scale parameters used were 0.4 to 0.55 by steps of 0.01. I also tested the findFaces on a few of my own photos, but the results were fairly unimpressive.In most of the photos there were illumination differences, chaotic backgrounds, tilted faces and all images were hi-res. The algorithm took too long to run more than a few parameter tests on each (which took a few hours alone), so it was difficult to quickly hone in on good scale values to use.

<figure class="half">
    <img src="/images/facial-detection-and-recognition/14.webp">
    <img src="/images/facial-detection-and-recognition/15.webp">
</figure>

## Verifying Faces

I used a trial and error approach incrementing up and down from the base 60000 MSE. I tried 40000 and 75000. The error rates are shown in the figure above. I found that the default 60000 was the superior MSE value to use because it produced 0 false positives and the smallest number of false negatives. Increasing the MSE value produced equivalent false negatives, but it also increased the false positives as expected. For this reason I stick by the default 60000 being the ideal.

![placeholder](/images/facial-detection-and-recognition/16.webp){:.align-center}

## What worked well and what did not?

Finding faces worked very well for shaved faced males on a plain background. It did not work as well for the interesting faced female photos, nor individuals with facial hair. I suspect that including some skin detection or color dependence in the algorithm may have helped. Using the find faces function on my non-reference group photos yielded unfavorable results. I suspect that this was because of the poor photos i chose to use as tests, but also because of the lack of any skin recognition in my algorithm. I think my algorithm was fairly limited to the trained data set. 


