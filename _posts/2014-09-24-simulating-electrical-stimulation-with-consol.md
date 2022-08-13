---
title: "Simulating Electrical Stimulation w/ Comsol"
date: 2014-09-24T00:00:00-00:00
last_modified_at: 2014-09-24T00:00:00-00:00
categories:
  - quantitative physiology
  - biomedical engineering
  - school project
permalink: /post-bme-simulating-electrical-stimulation-with-consol/
classes: wide
excerpt: Investigating the use of finite element solvers in basic electrode design and analysis.
header:
  og_image: /images/qp-computational/comsol-preview.jpg
  teaser: /images/qp-computational/comsol-preview.jpg
---


Comsol is a finite element solver and applications in various engineering problems. I investigate its use in basic electrode design and analysis.

## Effects of Various Electrode Configurations on Activation Functions

![preview](/images/qp-computational/comsol-preview-2.jpg){:.align-right}

In the following writeup I investigate the effects of various stimulation on activation functions for nearby axons.

1. I create a spherical electrode centered inside a much larger cylinder. Grounding all surfaces of the cylinder, I show the voltage on axons traveling down the length of the cylinder that are 0,5mm, 1.0mm and 2mm away from the center of the electrode. I also show scaled version of the 1st and 2nd spatial derivatives on the same plots as the voltage.
2. I repeat the procedure using bipolar stimulation, varying the distance between the two electrodes.
3. I repeat the procedure using tripolar stimulation, again experimenting with electrode locations to find a good combination for a strong activation function. 
4. Lastly I provide commentary on the differences between unipolar, bipolar and triplor stimulation, concluding that multi-polar stimulation setups can provide much more efficient activating functions.

{:.text-justify}

<object data="/images/qp-computational/simulating-electrical-stimulation.pdf" width="1000" height="1000" type="application/pdf"></object>

## Basic electrode design and analysis

![preview](/images/qp-computational/comsol-preview.jpg){:.align-center}

<object data="/images/qp-computational/simulating-electrical-stimulation-2.pdf" width="1000" height="1000" type="application/pdf"></object>
