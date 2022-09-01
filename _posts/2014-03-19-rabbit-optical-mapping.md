---
title: "Imaging -Rabbit Optical Mapping"
date: 2014-03-19T00:00:00-00:00
last_modified_at: 2014-03-19T00:00:00-00:00
categories:
  - quantitative physiology
  - biomedical engineering
  - school project
permalink: /post-bme-rabbit-optical/
classes: wide
excerpt: Computing signal characteristics of optical data to measure electrical arrhythmia in rabbits.
header:
  og_image: /images/qp-computational/rabbit-preview.jpg
  teaser: /images/qp-computational/rabbit-preview.jpg
---

![preview](/images/qp-computational/rabbit-preview.jpg){:.align-right}

Using recordings from an animal model of arrhythmia, Matlab code was developed to read the data, compute various signal characteristics and finally provide measures of electrical activity of normal rhythm and arrhythmia.

Data Format:

Optical mapping with voltage sensitive dyes arranged as 16-bit ints by frames, 264 channels each: 256 optical data points and 8 electrograms.  Sampling rate 1kHz, stimulus applied at 0msec.

{:.text-justify}

## Writeup

{% include pdf-embed.html url="/images/qp-computational/rabbit-optical-mapping.pdf" %}
