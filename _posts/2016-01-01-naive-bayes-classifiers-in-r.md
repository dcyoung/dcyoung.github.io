---
title: "Naive Bayes Classifier in R"
date: 2016-01-01T00:00:00-00:00
last_modified_at: 2016-01-01T00:00:00-00:00
categories:
  - machine learning
  - ai
  - school project
permalink: /post-naive-bayes-classifiers-in-r/
classes: wide
toc: True
excerpt: Writing a naive bayes classifier from scrach in R.
header:
  og_image: /images/logos/r.png
  teaser: /images/logos/r.png
---

## Dataset

The following code snippets were written to deal with the "Pima Indians" dataset: a famous collection of data on whether a patient has diabetes hosted by the UC Irvine learning data repository. The dataset can be obtained here: [​https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes](​https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes)

## Naive Bayes Classifier

A simple naive bayes classifier was written from scratch to classify this data set. 20% of the data was used for evaluation, and the other 80% for training. A normal distribution was used to model each of the class-conditional distributions. Over 20 completely separate training/testing trials with a different data split each trial, the average performance of the classifier was 74.67%.

```r
#clear the workspace and console
rm(list=ls())
cat("\014") #code to send ctrl+L to the console and therefore clear the screen
#setup working directory 
setwd('~/../DirectoryNameGoesHere')
#read all the data into a single table
allData <- read.csv('data.txt', header = FALSE) 
#import libraries to help with data splitting/partitioning etc.May not be used
library(klaR)
library(caret)
 
allFeatures<-allData[,-c(9)] #features
labels<-allData[,9] #labels
#partition the data (80% training, 20% testing)
trainingData <- createDataPartition(y=labels, p=.8, list=FALSE)
 
#---------------------------- IGNORE ANY MISSING VALUES -------------------------------------------
features <- allFeatures
 
#grab the subsets of features and labels from the 80% of data used for training
trainingFeatures <- features[trainingData, ]
trainingLabels <- labels[trainingData]
 
#partition the training data by class (labeled class)
trainingPositiveFlag <- trainingLabels > 0
posTrainingExamples <- trainingFeatures[trainingPositiveFlag, ]
negTrainingExamples <- trainingFeatures[!trainingPositiveFlag,]
 
#calcualte the means and standard deviations for both sets (pos and neg) of examples
posTrainingMeans <- sapply(posTrainingExamples, mean, na.rm=TRUE)
negTrainingMeans <- sapply(negTrainingExamples, mean, na.rm=TRUE)
posTrainingStdDev <- sapply(posTrainingExamples, sd, na.rm=TRUE)
negTrainingStdDev <- sapply(negTrainingExamples, sd, na.rm=TRUE)
 
#calculate the likelihoods (class conditional probabilities)
#use the means and std dev to calc the logarithmic sum of all the class conditional probabilities
posTrainingOffsets <- t(t(trainingFeatures)-posTrainingMeans)
posTrainingScaledOffsets <- t(t(posTrainingOffsets)/posTrainingStdDev)
posTrainingLogs <--(1/2)*rowSums(apply(posTrainingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(posTrainingStdDev))
 
negTrainingOffsets <- t(t(trainingFeatures)-negTrainingMeans)
negTrainingScaledOffsets <- t(t(negTrainingOffsets)/negTrainingStdDev)
negTrainingLogs <--(1/2)*rowSums(apply(negTrainingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(negTrainingStdDev))
 
#use the simplified decision rule for a 0-1 decision case
classifiedTrainingEgs <- posTrainingLogs > negTrainingLogs
#check against known labels to see where the classifications were accurate
correctClassifiedTrainEgs <- classifiedTrainingEgs==trainingLabels
#calculate the classification accuracy for this fold, and store it
train_accuracy_IGNORE_NA <- sum(correctClassifiedTrainEgs)/(sum(correctClassifiedTrainEgs)+sum(!correctClassifiedTrainEgs))
 
#----------Classify the testing data using the means and std deviations from the training data-----------
#use the other 20% of data (untouched) as a testing set
testingFeatures <- features[-trainingData, ]
testingLabels <- labels[-trainingData]
 
#calculate the likelihoods (class conditional probabilities)
# but this time, use the means and std dev FROM THE TRAINING DATA 
# to calc the logarithmic sum of all the class conditional probabilities
posTestingOffsets <- t(t(testingFeatures)-posTrainingMeans)  #use the training data means
posTestingScaledOffsets <- t(t(posTestingOffsets)/posTrainingStdDev) #use the training data std dev
posTestingLogs <--(1/2)*rowSums(apply(posTestingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(posTrainingStdDev)) #use the training data std dev
negTestingOffsets <- t(t(testingFeatures)-negTrainingMeans)
negTestingScaledOffsets <- t(t(negTestingOffsets)/negTrainingStdDev)
negTestingLogs <--(1/2)*rowSums(apply(negTestingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(negTrainingStdDev))
 
#use the simplified decision rule for a 0-1 decision case
classifiedTestingEgs <- posTestingLogs > negTestingLogs
#check against known labels to see where the classifications were accurate
correctClassifiedTestEgs <- classifiedTestingEgs == testingLabels
#calculate the classification accuracy for this fold, and store it
test_accuracy_IGNORE_NA <- sum(correctClassifiedTestEgs)/(sum(correctClassifiedTestEgs)+sum(!correctClassifiedTestEgs))
```

## Naive Bayes Classifier Modifications

After running the previous classifier, the code was adjusted to account for a few of the patient attributes containing missing values for some examples.  Using the exact same 20 data splits from the unmodified bayes classifier above, the version that acknowledged missing values had an average classification accuracy of 73.89%. Recall the accuracy of the unmodified version which ignored missing values was 74.67%. Surprisingly, for most trials, the classification accuracy actually dropped when considering the missing values. I would have expected an improvement. The drop wasn't large (~1-2%) but it was noticeable. One possible explanation for this decrease is that the naive bayes model was implemented using a normal distribution to model the features, which is a very inaccurate assumption. When including missing values as 0's (1st classifier) the normal distribution is skewed to the left inaccurately. When removing the missing values from features with many missing examples (modification), the mean shifts to the right. Because the class-conditional probability distributions were heavily skewed, the unmodified classifier might have yielded a higher accuracy.

```r
#----------------------------NOW ACKNOWLEDGE THE MISSING VALUES ------------------------------------
 
#adjust the features such that a 0 is reported as "NA"
#for each feature in question (3,4,6 and 8)
for (f in c(3, 4, 6, 8))
{
  #determine which examples had a 0 for this feature (ie: unknown value)
  examplesMissingFeatureF <- allFeatures[, f] == 0
  #replace all these missing values with an NA
  features[examplesMissingFeatureF, f] = NA
}
 
#grab the subsets of features and labels from the 80% of data used for training
trainingFeatures <- features[trainingData, ]
trainingLabels <- labels[trainingData]
 
#partition the training data by class (labeled class)
trainingPositiveFlag <- trainingLabels > 0
posTrainingExamples <- trainingFeatures[trainingPositiveFlag, ]
negTrainingExamples <- trainingFeatures[!trainingPositiveFlag,]
 
#calcualte the means and standard deviations for both sets (pos and neg) of examples
posTrainingMeans <- sapply(posTrainingExamples, mean, na.rm=TRUE)
negTrainingMeans <- sapply(negTrainingExamples, mean, na.rm=TRUE)
posTrainingStdDev <- sapply(posTrainingExamples, sd, na.rm=TRUE)
negTrainingStdDev <- sapply(negTrainingExamples, sd, na.rm=TRUE)
 
#calculate the likelihoods (class conditional probabilities)
#use the means and std dev to calc the logarithmic sum of all the class conditional probabilities
posTrainingOffsets <- t(t(trainingFeatures)-posTrainingMeans)
posTrainingScaledOffsets <- t(t(posTrainingOffsets)/posTrainingStdDev)
posTrainingLogs <--(1/2)*rowSums(apply(posTrainingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(posTrainingStdDev))
 
negTrainingOffsets <- t(t(trainingFeatures)-negTrainingMeans)
negTrainingScaledOffsets <- t(t(negTrainingOffsets)/negTrainingStdDev)
negTrainingLogs <--(1/2)*rowSums(apply(negTrainingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(negTrainingStdDev))
 
#use the simplified decision rule for a 0-1 decision case
classifiedTrainingEgs <- posTrainingLogs > negTrainingLogs
#check against known labels to see where the classifications were accurate
correctClassifiedTrainEgs <- classifiedTrainingEgs==trainingLabels
#calculate the classification accuracy for this fold, and store it
train_accuracy_ACKNOWLEDGE_NA <- sum(correctClassifiedTrainEgs)/(sum(correctClassifiedTrainEgs)+sum(!correctClassifiedTrainEgs))
 
#----------Classify the testing data using the means and std deviations from the training data-----------
#use the other 20% of data (untouched) as a testing set
testingFeatures <- features[-trainingData, ]
testingLabels <- labels[-trainingData]
 
#calculate the likelihoods (class conditional probabilities)
# but this time, use the means and std dev FROM THE TRAINING DATA 
# to calc the logarithmic sum of all the class conditional probabilities
posTestingOffsets <- t(t(testingFeatures)-posTrainingMeans)  #use the training data means
posTestingScaledOffsets <- t(t(posTestingOffsets)/posTrainingStdDev) #use the training data std dev
posTestingLogs <--(1/2)*rowSums(apply(posTestingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(posTrainingStdDev)) #use the training data std dev
negTestingOffsets <- t(t(testingFeatures)-negTrainingMeans)
negTestingScaledOffsets <- t(t(negTestingOffsets)/negTrainingStdDev)
negTestingLogs <--(1/2)*rowSums(apply(negTestingScaledOffsets,c(1, 2), function(x)x^2), na.rm=TRUE)-sum(log(negTrainingStdDev))
 
#use the simplified decision rule for a 0-1 decision case
classifiedTestingEgs <- posTestingLogs > negTestingLogs
#check against known labels to see where the classifications were accurate
correctClassifiedTestEgs <- classifiedTestingEgs == testingLabels
#calculate the classification accuracy for this fold, and store it
test_accuracy_ACKNOWLEDGE_NA <- sum(correctClassifiedTestEgs)/(sum(correctClassifiedTestEgs)+sum(!correctClassifiedTestEgs))
```

## Package Based Naive Bayes Classifier

Now, a naive bayes classifier was constructed using the klaR and caret packages. The caret package was used for cross-validation while the klaR package was used to estimate the class-conditional densities using a density estimation procedure. This classifier assumes no attribute has a missing value. 

The average over 20 different data split trials was 75.85%. So, allowing a more optimized package to construct the naive bayes model yielded slightly improved performance. The performance gains here can be attributed to the models used for the features. The packages are free to use models other than a normal distribution which is likely more accurate for some features.

```r
#read all the data into a single table
allData <- read.csv('data.txt', header = FALSE) 
 
#import libraries to help with data splitting/partitioning, 
#cross validation and easy classifier construction
library(klaR)
library(caret)
 
#grab the features from the main data file, removing the labels 
#assume no data is missing... ie: ignore missing values without noting them as NA
features <- allData[,-c(9)]
 
#grab the labels from the main data file... use as.factor to make 
#the format comptabile with future functions to be used
labels <- as.factor(allData[,9])
 
#split the data into 80% training data and 20% testing data
trainingData <- createDataPartition(y=labels, p=.8, list=FALSE)
 
trainingFeatures <- features[trainingData,]
trainingLabels <- labels[trainingData]
testingFeatures <- features[-trainingData,]
testingLabels <- labels[-trainingData]
 
#Fit Predictive Models over Different Tuning Parameters
#in this case...
#   use a naive bayes model for the classifier ('nb')
#   use cross validation resampling method with 10 folds/resampling iterations ('cv')
classifierModel <- train(trainingFeatures, trainingLabels, 'nb', trControl = trainControl(method='cv', number=10))
 
#use the trained model to predict class labels for the testing data
#note: argument newdata specifies the first place to look for explanatory variables to be used for prediction
predictedLabels <- predict(classifierModel, newdata = testingFeatures)
 
#compare the predicted labels to the actual known labels for the testing data
confusionMatrix(data = predictedLabels, testingLabels)
```

## Comparing to SVMLight

SVMLight and klaR were used to train an SVM (support vector machine) to classify the same data. 20% of the data was held out for testing while the other 80% was used for training. 

The average classification accuracy over 20 separate data split trials was 76.34%. Again there was a small performance improvement, even over the more optimized naive bayes classifier. The SVM classifier abstracts the parameters that model specific distributions into weights and values that are free to adjust to the training data more than the statistical models can permit. Provided enough training data, this yields very good results.

```r
#read all the data into a single table
allData <- read.csv('data.txt', header = FALSE) 
 
#import libraries to help with data splitting/partitioning, 
#cross validation etc.
library(klaR)
library(caret)
 
#grab the features from the main data file, removing the labels 
#assume no data is missing... ie: ignore missing values without noting them as NA
features <- allData[,-c(9)]
 
#grab the labels from the main data file... use as.factor to make 
#the format comptabile with future functions to be used
labels <- as.factor(allData[,9])
 
#split the data into 80% training data and 20% testing data
trainingData <- createDataPartition(y=labels, p=.8, list=FALSE)
 
trainingFeatures <- features[trainingData,]
trainingLabels <- labels[trainingData]
testingFeatures <- features[-trainingData,]
testingLabels <- labels[-trainingData]
 
#train an svm using the training data 
svm<-svmlight(trainingFeatures, trainingLabels)
 
#use the trained svm model to predict classes for the testing features
predictedLabels <- predict(svm, testingFeatures)
 
#determine where the classifications were correct
correctClassifications <- predictedLabels$class
 
#calculate the accuracy of the classifier
sum(correctClassifications==testingLabels)/(sum(correctClassifications==testingLabels)+sum(!(correctClassifications==testingLabels)))
```