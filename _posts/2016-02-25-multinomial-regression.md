---
title: "Multinomial Regression on Wide Datasets"
date: 2016-02-25T00:00:00-00:00
last_modified_at: 2016-02-25T00:00:00-00:00
categories:
  - machine learning
  - ai
  - school project
permalink: /post-multinomial-regression/
classes: wide
toc: True
excerpt: Classification for “wide” datasets, w/ more features than examples.
header:
  og_image: /images/logos/r.png
  teaser: /images/logos/r.png
---

## Dataset

The authors of  "Clustering Cancer Gene Expression Data: a Comparative Study", clustered gene expression data for various cancers. Each of the 35 data sets is “wide” meaning it has more predictors than examples, and in this case many more predictors than examples (typically more than 1000 predictors and less than 100 examples). My goal was to assign a class from a subset of various medical issues. Each data set has a different number of possible classes, between 2 and 14.

The actual data can be found here:
[http://bioinformatics.rutgers.edu/Static/Supplements/CompCancer/datasets.htm](http://bioinformatics.rutgers.edu/Static/Supplements/CompCancer/datasets.htm)

A more detailed description of the data can be found here:
[http://bioinformatics.rutgers.edu/Supplements/CompCancer/](http://bioinformatics.rutgers.edu/Supplements/CompCancer/)

## Implementation

Github repo available here: [https://github.com/dcyoung/MultinomialRegression](https://github.com/dcyoung/MultinomialRegression)

​First the datasets were checked for missing or non-numeric values. Only 1 dataset contained such values and they were replaced by zeros. Experimentation with further pre-processing (dimensionality reduction via PCA) did not yield better performance, but actually decreased performance. Because of this, the number of predictors was left intact and fed to the regression where the lasso would effectively prune unnecessary predictors.

For each dataset, a multinomial regression model with the lasso was constructed and used to predict the relevant classes. At first the loss for cross-validation was left at its default type.measure of “deviance” which uses the squared-error for Gaussian models. While this was producing 100% training accuracy, the cv.glment cross validation error for the best model was not optimal. Changing the loss type.measure to “class” forced the package to use the misclassification error (only suitable for binomial or multinomial regression). Using the misclassification error for loss drastically improved the cross validation error for the best model. There were many cases where the error dropped from around 30% to less than 10%.

Sometimes, the best model yielded a misclassification error that was only slightly better than a model which used far fewer coefficients. Depending on the application, model complexity may be more important than absolute lowest misclassification error. If that is the case, one might wish to examine a plot of misclassification rate vs. regularization constant (representing # of included coefficients) and choose by hand which model strikes the right balance between complexity and performance. For these data sets however, complexity was not greatly affecting runtime, so the model which yielded the lowest misclassification error was chosen in all cases.
​
More specifically, the model was chosen by selecting the regularization constant which yielded the lowest misclassification error. The number of genes used in the model is represented by the number of coefficients included in the model at that regularization constant.

## Results

The results for each data set are outlined in the following table. I’ve included the chosen regularization constant, the training error and a ratio of the # of included genes/ # of classes. Lastly I included an average at the bottom. Some of the average values are relatively meaningless given the diversity of the dataset parameters, but some are noteworthy. The average CV misclassification error was around 12%, which is impressive given how wide the datasets were. This is a really powerful technique!  The average training error was around 2-3% which just confirms the model was building correctly, while the misclassification error is a better representation of its performance. The average ratio of #genes/#classes is a little over 4. Meaning on average a model required 4x as many non-zero coefficients (or predictive genes) as it had classes from which to classify. This must be taken with a large grain of salt however… as described previously, for some data sets the best model performed only slightly better than a much simpler model. Choosing a good balance of complexity to performance would yield a more representative average of # of genes/# of classes. But I thought I would include the statistic anyways, as it is interesting.

Data Base File Name:|# of Classes|Regularization Constant (Lambda) for best model|Coefficients (# included genes)|Cross Validation Misclassification Error|Training Error|Ratio #Genes/#Classes
:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:
alizadeh-2000-v1_database.txt|2|0.01916398|24|0.09523810|0.00000000|12.00
alizadeh-2000-v2_database.txt|3|0.12037204|5|0.01612903|0.00000000|1.67
alizadeh-2000-v3_database.txt|4|0.06157294|11|0.08064516|0.00000000|2.75
armstrong-2002-v1_database.txt|2|0.08594995|9|0.05555556|0.01388889|4.50
armstrong-2002-v2_database.txt|3|0.01195216|14|0.08333333|0.00000000|4.67
bhattacharjee-2001_database.txt|5|0.00702128|10|0.07389163|0.00000000|2.00
bittner-2000_database.txt|2|0.00549008|20|0.10526316|0.00000000|10.00
bredel-2005_database.txt|3|0.02097127|11|0.14000000|0.00000000|3.67
chen-2002_database.txt|2|0.02845673|18|0.03910615|0.01675978|9.00
chowdary-2006_database.txt|2|0.07596433|6|0.01923077|0.01923077|3.00
dyrskjot-2003_database.txt|3|0.05072785|9|0.22500000|0.00000000|3.00
garber-2001_database.txt|4|0.11605594|4|0.15151515|0.12121212|1.00
golub-1999-v1_database.txt|2|0.02017088|19|0.05555556|0.00000000|9.50
golub-1999-v2_database.txt|3|0.12477965|5|0.05555556|0.04166667|1.67
gordon-2002_database.txt|2|0.02947920|16|0.02209945|0.00000000|8.00
khan-2001_database.txt|4|0.13232613|5|0.01204819|0.00000000|1.25
laiho-2007_database.txt|2|0.11268743|13|0.13513514|0.02702703|6.50
lapointe-2004-v1_database.txt|3|0.08378991|9|0.19117647|0.04411765|3.00
lapointe-2004-v2_database.txt|4|0.02441359|19|0.16513762|0.00000000|4.75
liang-2005_database.txt|3|0.12153683|1|0.02702703|0.00000000|0.33
nutt-2003-v1_database.txt|4|0.00630569|14|0.34000000|0.00000000|3.50
nutt-2003-v2_database.txt|2|0.00471073|17|0.17857143|0.00000000|8.50
nutt-2003-v3_database.txt|2|0.35731114|3|0.27272727|0.31818182|1.50
pomeroy-2002-v1_database.txt|2|0.02637890|14|0.05882353|0.00000000|7.00
pomeroy-2002-v2_database.txt|5|0.07076972|7|0.23809524|0.00000000|1.40
ramaswamy-2001_database.txt|14|0.02225367|8|0.30000000|0.07368421|0.57
risinger-2003_database.txt|4|0.06281940|6|0.14285714|0.00000000|1.50
shipp-2002-v1_database.txt|2|0.10239171|15|0.16883117|0.15584416|7.50
singh-2002_database.txt|2|0.09746390|7|0.05882353|0.06862745|3.50
su-2001_database.txt|10|0.02999744|7|0.08620690|0.00574713|0.70
tomlins-2006_database.txt|5|0.03332642|18|0.18269231|0.00961539|3.60
tomlins-2006-v2_database.txt|4|0.04036825|12|0.14130435|0.00000000|3.00
west-2001_database.txt|2|0.06085212|14|0.12244898|0.00000000|7.00
yeoh-2002-v1_database.txt|2|0.00587707|16|0.00806452|0.00000000|8.00
yeoh-2002-v2_database.txt|6|0.02372582|12|0.12903226|0.01209677|2.00
Average:|3.54|0.06278383|11.37|0.1193|0.0265|4.33
