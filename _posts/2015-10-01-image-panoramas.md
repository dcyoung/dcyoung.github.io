---
title: "360 Panoramas (Alignment, Stitching, Blending)"
date: 2015-10-01T00:00:00-00:00
last_modified_at: 2015-10-01T00:00:00-00:00
categories:
  - computer vision
  - school project
permalink: /post-image-panoramas/
classes: wide
toc: True
excerpt: Creating 360 panoramas from a set of images.
header:
  og_image: /images/image-panoramas/0.jpg
  teaser: /images/image-panoramas/0.jpg
---

## Creating Panoramas

The idea behind this project was to take a set of images (about 15-20) and create a panorama of a full 360 degree scene. The code written previously to detect and describe features (I've described that fully elsewhere on the website) can serve as the foundation of a panorama generator. The code shown here is just an outline for the panorama generating portions of the pipeline.

## Overview + Major Design Choices

The general process is as follows:

- Warp each image into spherical coordinates.
- Determine the features for each warped image. (click HERE to see Feature Detection and HERE to see feature Description)
- Match features between every pair of adjacent images. (click HERE to see Feature Matching)
- Align every pair of adjacent images using RANSAC.
- Blend the aligned images to create a panorama.

## Resulting Panoramas

A few different panorama's were generated and the results are shown below. The first is the result of images available in similar project packages around the web, I did not take the source images for the 1st panorama. The 2nd and 3rd panoramas are of the main entrance to Wash U, with and without me in the photos.  The 3rd and 4th panoramas are of the Kemper art museum on Wash U campus with and without my friend Robert in the photos. The alignment and corrections are working well, but this could use a more robust mechanism to account for changes in illumination between adjacent photos.

[![panorama](/images/image-panoramas/0.jpg){:.align-center}](/images/image-panoramas/0.jpg)
[![panorama](/images/image-panoramas/1.jpg){:.align-center}](/images/image-panoramas/1.jpg)
[![panorama](/images/image-panoramas/2.jpg){:.align-center}](/images/image-panoramas/2.jpg)
[![panorama](/images/image-panoramas/3.jpg){:.align-center}](/images/image-panoramas/3.jpg)
[![panorama](/images/image-panoramas/4.jpg){:.align-center}](/images/image-panoramas/4.jpg)

## Removing Radial Distortion & Warping Images to Spherical Coordinates

The following method contains all the logic for warping an image to spherical coordinates as well as applying a radial distortion.

```cpp
CFloatImage WarpSphericalField(CShape srcSh, CShape dstSh, float f, float k1, float k2, const CTransform3x3 &r)
	{
		// Set up the pixel coordinate image
		dstSh.nBands = 2;
		CFloatImage uvImg(dstSh);   // ( u,v ) coordinates

		// Fill in the values
		for (int y = 0; y < dstSh.height; y++)
		{
			float *uv = &uvImg.Pixel(0, y, 0);
			for (int x = 0; x < dstSh.width; x++, uv += 2)
			{
				// (x,y) is the spherical image coordinates. 
				// (xf,yf) is the spherical coordinates, e.g., xf is the angle theta
				// and yf is the angle phi

				float xf = (x - 0.5f*dstSh.width ) / f;
				float yf = (y - 0.5f*dstSh.height) / f;

				// (xt,yt,zt) are intermediate coordinates to which you can
				// apply the spherical correction and radial distortion
				float xt, yt, zt;
				CVector3 p;
	 
		
				// apply the spherical correction, i.e.,
				// compute the Euclidean coordinates, rotate according to
				// r, and project the point to the z=1 plane at
				// (xt/zt,yt/zt,1), then distort with radial distortion
				// coefficients k1 and k2

				//convert the theta and phi to spherical coordinates 
				p[0] = sin(xf)*cos(yf);
				p[1] = sinf(yf);
				p[2] = cos(xf)*cos(yf);

				//p = r*p; //p now holds the rotated spherical coordinates ?

				//normalize all the coordinates by z_hat
				xt = p[0] / p[2];
				yt = p[1] / p[2];
				zt = 1;
				
				//apply radial distortion
				float r_squared = xt*xt + yt*yt;
				xt = xt*(1 + k1*r_squared + k2*r_squared*r_squared);
				yt = yt*(1 + k1*r_squared + k2*r_squared*r_squared);

				// Convert back to regular pixel coordinates and store
				float xn = 0.5f*srcSh.width  + xt*f;
				float yn = 0.5f*srcSh.height + yt*f;
				uv[0] = xn;
				uv[1] = yn;
			}
		}
		return uvImg;
	}
```

## Aligning Warped Images using RANSAC

The followings code assumes the images warped by the previous code have undergone feature detection and description. That process  could be accomplished using code I've written in previous projects, or using state of the art approaches like SIFT. The following controller code functionally selects a random matching pair of features and computes the translation between the two feature locations. Then it calls countInliers to count how many matches agree with the estimate translation of f1 to f2. Repeating this nRANSAC times and keeping track of the best estimate (by number of inliers) is a good estimation. But to further define the exact value beyond an integer pixel, I sent the result off to leastSquaresFit which performs a least squares fit to determine an even better estimate.

```cpp
int alignPair(const FeatureSet &f1, const FeatureSet &f2,
	  const vector &matches, MotionModel m, float f,
	  int nRANSAC, double RANSACthresh, CTransform3x3& M)
{
	int bestIndex;   // holds index of match with most inclusive translation
	int testIndex;	 // holds current index being tested for number of inliers
	vector bestIndexAssociatedInliers; //the indices of matches that follow the same translation as the bestIndex
	int bestInlierCount = 0; //number of inliers in bestIndexAssociatedInliers
	
	FeatureMatch match;
	int xTrans, yTrans;
	Feature feature1, feature2;
	CTransform3x3 transMatrix;
	
	
	/*repeat the following cycle:
		1. pick a random feature pair (ie: a feature and its match from the other image)
		2. determine the translation (ie: change in x and y that would be required to make 
			the coordinates of f1 equal to the coordinates of its match)
			for ex: if f1 was at pixel 4,7 and f2 was at pixel 5,8 in its coordinate space, then the required translation owuld be +1,+1
		3. apply that translation to every feature in f1Set and see if it is within tolerance of its match from f2Set
		4. if it is close enough to f2, count it as an inlier, if it isn't, do not count it. 
		5. keep track of the translation and the number of inliers.
	*/

	for (int i = 0; i < nRANSAC; i++){

		testIndex = rand() % matches.size(); // provides a random index between 0 and the size of matches	

		feature1 = f1[matches[testIndex].id1 - 1];
		feature2 = f2[matches[testIndex].id2 - 1];

		xTrans = feature2.x - feature1.x;
		yTrans = feature2.y - feature1.y;
		
		transMatrix = CTransform3x3::Translation((float) xTrans, (float) yTrans);
		
		vector inliers;
		int count = countInliers(f1, f2, matches, m, f,transMatrix, RANSACthresh, inliers);

		if (count > bestInlierCount){
			bestIndex = i;
			bestInlierCount = count;
			bestIndexAssociatedInliers = inliers;
			M = transMatrix;
		}

	}
	
	leastSquaresFit(f1, f2,matches, m, f, bestIndexAssociatedInliers, M);

	return 0;
}
```

Counting inliers is fairly straightforward. For the given estimation, each possibility is checked against a threshold and a count is increased if the match is an inlier.

```cpp
int countInliers(const FeatureSet &f1, const FeatureSet &f2,
	 const vector &matches, MotionModel m, float f,
	 CTransform3x3 M, double RANSACthresh, vector &inliers)
{
	inliers.clear();
	int count = 0;
	for (unsigned int i=0; i<(int) matches.size(); i++) {
		
		// determine if the ith matched feature f1[id1-1], when transformed by M,
		// is within RANSACthresh of its match in f2
		//
		// if so, increment count and append i to inliers
		//
		// *NOTE* Each match contains two feature ids of matching features, id1 and id2.
		//        These ids are 1-based indices into the feature arrays,
		//        so access the appropriate features as f1[id1-1] and f2[id2-1].


		CVector3 feat1Vec = CVector3();
		Feature testF1 = f1[matches[i].id1 - 1];
		Feature testF2 = f2[matches[i].id2 - 1];

		feat1Vec[0] = testF1.x;
		feat1Vec[1] = testF1.y;
		feat1Vec[2] = 1;

		CVector3 translatedF1 = M*feat1Vec;
		float dx = testF2.x - translatedF1[0];
		float dy = testF2.y - translatedF1[1];
		float distError = sqrt(dx*dx+dy*dy);
		if (distError <= RANSACthresh){
			inliers.push_back(i);
			count++;
		}
	}
	return count;
}
```

Performing a least Squares Fit here is simple because of the restricted degrees of freedom. The average translation vector yields the result.

```cpp
int leastSquaresFit(const FeatureSet &f1, const FeatureSet &f2,
		const vector &matches, MotionModel m, float f,
		const vector &inliers, CTransform3x3& M)
{

	// for panoramas the transformation is a translation and
	// only has two degrees of freedom
	//
	// therefore, simply compute the average translation vector
	// between the feature in f1 and its match in f2 for all inliers
	double u = 0;
	double v = 0;
	
	for (int i=0; i < inliers.size(); i++) {
		double xTrans, yTrans;

		// compute the translation implied by the ith inlier match
		// and store it in (xTrans,yTrans)

	
		Feature testF1 = f1[matches[inliers[i]].id1 - 1];
		Feature testF2 = f2[matches[inliers[i]].id2 - 1];
		
		xTrans = testF2.x - testF1.x;
		yTrans = testF2.y - testF1.y;

	
		u += xTrans;
		v += yTrans;
	}

	u /= inliers.size();
	v /= inliers.size();

	M[0][0] = 1;
	M[0][1] = 0;
	M[0][2] = -u;
	M[1][0] = 0;
	M[1][1] = 1;
	M[1][2] = -v;
	M[2][0] = 0;
	M[2][1] = 0;
	M[2][2] = 1;

	return 0;
}
```

## Stitch and Crop the Resulting Aligned Image

The basic outline here is to stitch the aligned images. Given warped images and their displacements, I figure out the max and min corners to determine the overall dimensions of the panorama. I also determine the absolute displacements of each image in the final panorama coordinate space given their relative displacements from each other. This is all accomplished in blendImages. Then I blend each image with its adjacent images in the panorama in AccumulateBlend and Normalize Blend. Here i use a feathering function that is simply a ratio equal to the slope of a line defined by the blendwidth. Technically this is a 1d version of a distance map. Normalizing the blend occurs after the feathering. Finally the resulting image is transformed using a an affine shear matrix, because in this case the only translation is in the y direction. Therefore a shear can revert things back to normal.

### Determining the Absolute Bounds of the Panorama + Blending Images

```cpp
CByteImage BlendImages(CImagePositionV& ipv, float blendWidth)
{
	// Assume all the images are of the same shape (for now)
	CByteImage& img0 = ipv[0].img;
	CShape sh        = img0.Shape();
	int width        = sh.width;
	int height       = sh.height;
	int nBands       = sh.nBands;
	int dim[2]       = {width, height};
	

	// Compute the bounding box for the mosaic
	int n = ipv.size();
	float min_x = 0, min_y = 0;
	float max_x = 0, max_y = 0;
	int i;
	for (i = 0; i < n; i++)
	{
		
		CTransform3x3 &pos = ipv[i].position;

		CVector3 corners[4];

		corners[0][0] = 0.0;
		corners[0][1] = 0.0;
		corners[0][2] = 1.0;

		corners[1][0] = width - 1;
		corners[1][1] = 0.0;
		corners[1][2] = 1.0;

		corners[2][0] = 0.0;
		corners[2][1] = height - 1;
		corners[2][2] = 1.0;

		corners[3][0] = width - 1;
		corners[3][1] = height - 1;
		corners[3][2] = 1.0;

		corners[0] = pos * corners[0];
		corners[1] = pos * corners[1];
		corners[2] = pos * corners[2];
		corners[3] = pos * corners[3];

		corners[0][0] /= corners[0][2];
		corners[0][1] /= corners[0][2];

		corners[1][0] /= corners[0][2];
		corners[1][1] /= corners[0][2];

		corners[2][0] /= corners[0][2];
		corners[2][1] /= corners[0][2];

		corners[3][0] /= corners[0][2];
		corners[3][1] /= corners[0][2];
		
		// update min_x, ..., max_y
		
		//check the corners to see if an x or y is smaller/larger than the running min/max and update the running version if so.
		min_x = (float)MIN(min_x, corners[0][0]);
		min_x = (float)MIN(min_x, corners[1][0]);
		min_x = (float)MIN(min_x, corners[2][0]);
		min_x = (float)MIN(min_x, corners[3][0]);

		min_y = (float)MIN(min_y, corners[0][1]);
		min_y = (float)MIN(min_y, corners[1][1]);
		min_y = (float)MIN(min_y, corners[2][1]);
		min_y = (float)MIN(min_y, corners[3][1]);

		max_x = (float)MAX(max_x, corners[0][0]);
		max_x = (float)MAX(max_x, corners[1][0]);
		max_x = (float)MAX(max_x, corners[2][0]);
		max_x = (float)MAX(max_x, corners[3][0]);

		max_y = (float)MAX(max_y, corners[0][1]);
		max_y = (float)MAX(max_y, corners[1][1]);
		max_y = (float)MAX(max_y, corners[2][1]);
		max_y = (float)MAX(max_y, corners[3][1]);
	}

	// Create a floating point accumulation image
	CShape mShape((int)(ceil(max_x) - floor(min_x)),
				  (int)(ceil(max_y) - floor(min_y)), nBands);
	CFloatImage accumulator(mShape);
	accumulator.ClearPixels();

	double x_init, x_final;
	double y_init, y_final;

	// Add in all of the images
	for (i = 0; i < n; i++) {
		
		CTransform3x3 &M = ipv[i].position;

		CTransform3x3 M_t = CTransform3x3::Translation(-min_x, -min_y) * M;

		CByteImage& img = ipv[i].img;

		// Perform the accumulation
		AccumulateBlend(img, accumulator, M_t, blendWidth);

		if (i == 0) {
			CVector3 p;
			p[0] = 0.5 * width;
			p[1] = 0.0;
			p[2] = 1.0;

			p = M_t * p;
			x_init = p[0];
			y_init = p[1];
		} else if (i == n - 1) {
			CVector3 p;
			p[0] = 0.5 * width;
			p[1] = 0.0;
			p[2] = 1.0;

			p = M_t * p;
			x_final = p[0];
			y_final = p[1];
		}
	}



	// Normalize the results
	CByteImage compImage(mShape);
	NormalizeBlend(accumulator, compImage);
	bool debug_comp = false;
	if (debug_comp)
		WriteFile(compImage, "tmp_comp.tga");

	// Allocate the final image shape
	CShape cShape(mShape.width - width, height, nBands);
	CByteImage croppedImage(cShape);

	// Compute the affine deformation
	CTransform3x3 A;

	// A will trim the left edge and take out the vertical drift
	
	
	//if (true){ /*the image is built from the left*/
		A[1][0] = -(min_y - max_y + height) / (max_x - min_x); //shear
	//}
	//else{ /*the image is built from the right, like the campus image set*/
	//	A[1][0] = (min_y - max_y + height) / (max_x - min_x); //shear
	//	A[1][2] = -(min_y - max_y + height); //y translation
	//}

	// Warp and crop the composite
	WarpGlobal(compImage, croppedImage, A, eWarpInterpLinear);

	return croppedImage;
}
```

### Accumulating the Blend

Here I blend each image with its adjacent images in the panorama using the feathering function outlined previously.

```cpp
static void AccumulateBlend(CByteImage& img, CFloatImage& acc, CTransform3x3 M, float blendWidth)
{
	/* Compute the bounding box of the image of the image */
	int bb_min_x, bb_min_y, bb_max_x, bb_max_y;
	ImageBoundingBox(img, M, bb_min_x, bb_min_y, bb_max_x, bb_max_y);

	CTransform3x3 Minv = M.Inverse();

	for (int y = bb_min_y; y <= bb_max_y; y++) {
		for (int x = bb_min_x; x < bb_max_x; x++) {
			/* Check bounds in destination */
			if (x < 0 || x >= acc.Shape().width || 
				y < 0 || y >= acc.Shape().height)
				continue;

			/* Compute source pixel and check bounds in source */
			CVector3 p_dest, p_src;
			p_dest[0] = x;
			p_dest[1] = y;
			p_dest[2] = 1.0;

			p_src = Minv * p_dest;

			float x_src = (float) (p_src[0] / p_src[2]);
			float y_src = (float) (p_src[1] / p_src[2]);

			if (x_src < 0.0 || x_src >= img.Shape().width - 1 ||
				y_src < 0.0 || y_src >= img.Shape().height - 1)
				continue;

			int xf = (int) floor(x_src);
			int yf = (int) floor(y_src);
			int xc = xf + 1;
			int yc = yf + 1;

			/* Skip black pixels */
			if (img.Pixel(xf, yf, 0) == 0x0 && 
				img.Pixel(xf, yf, 1) == 0x0 && 
				img.Pixel(xf, yf, 2) == 0x0)
				continue;

			if (img.Pixel(xc, yf, 0) == 0x0 && 
				img.Pixel(xc, yf, 1) == 0x0 && 
				img.Pixel(xc, yf, 2) == 0x0)
				continue;

			if (img.Pixel(xf, yc, 0) == 0x0 && 
				img.Pixel(xf, yc, 1) == 0x0 && 
				img.Pixel(xf, yc, 2) == 0x0)
				continue;

			if (img.Pixel(xc, yc, 0) == 0x0 && 
				img.Pixel(xc, yc, 1) == 0x0 && 
				img.Pixel(xc, yc, 2) == 0x0)
				continue;

			
			double weight = 1.0;
			// set weight according to a feathering function
									
			//use the triangle to find the feathered weight if your within the blendwidth
			//x_src and y_src are the coordinates of the pixel in the single image coordinate space
			//x and y are the coordinate of the pixel in the panorama coordinate space
			
			if (x_src < blendWidth){
				weight = x_src/blendWidth;
			}
			else if (x_src > img.Shape().width - blendWidth){
				weight = (img.Shape().width - x_src) / blendWidth;
			}
			
			if(y_src < blendWidth){
				weight = weight*(y_src / blendWidth);
			}
			else if (y_src > img.Shape().height - blendWidth){
				weight = weight*(img.Shape().height - y_src) / blendWidth;
			}

			acc.Pixel(x, y, 0) += (float) (weight * img.PixelLerp(x_src, y_src, 0));
			acc.Pixel(x, y, 1) += (float) (weight * img.PixelLerp(x_src, y_src, 1));
			acc.Pixel(x, y, 2) += (float) (weight * img.PixelLerp(x_src, y_src, 2));
			acc.Pixel(x, y, 3) += (float) weight;

		}
	}
}
```

### Normalizing the Blend

Here I normalize the blend which can be accomplished by simply dividing each color by the weight calculated in accumulate blend.

```cpp
static void NormalizeBlend(CFloatImage& acc, CByteImage& img)
{
	int height = acc.Shape().height;
	int width = acc.Shape().width;
	for (int x = 0; x < width; x++)
	{
		for (int y = 0; y < height; y++){
			img.Pixel(x, y, 0) = acc.Pixel(x, y, 0)/acc.Pixel(x, y, 3);
			img.Pixel(x, y, 1) = acc.Pixel(x, y, 1)/acc.Pixel(x, y, 3);
			img.Pixel(x, y, 2) = acc.Pixel(x, y, 2)/acc.Pixel(x, y, 3);
			//assume Pixel(x,y,3) is defaulted to one
		}
	}
}
```

## What worked well and what did not?

While testing the affine matrix transformation, the best results were obtained by using a shear matrix to deform the image as it was only shifted in the y direction. What did not work well was attempting to use a vertical translation calculated by the x coordinate because it was extremely difficult to figure out how to store that in a matrix. The affine shear matrix accomplishes the exact same thing, but with a more mathematical intuition than trying to determine it geometrically. Also the RANSAC worked extremely well even before applying a leastSquares best fit. But no harm in making it even better.
