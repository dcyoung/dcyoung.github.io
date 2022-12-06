---
title: "EKG Amplifier - Biological Signal Conditioning"
date: 2014-02-04T00:00:00-00:00
last_modified_at: 2014-02-04T00:00:00-00:00
categories:
  - quantitative physiology
  - biomedical engineering
  - school project
permalink: /post-bme-biological-signal-conditioning/
classes: wide
excerpt:  Constructing a simple analog EKG amplifier to produce clean Lead I EKG recordings with identifiable wave characteristics.
header:
  og_image: /images/qp-physical/biological-signal-conditioning.webp
  teaser: /images/qp-physical/biological-signal-conditioning.webp
---

 
## Abstract

EKG recordings can provide valuable information in diagnosing patient heart function, dysfunction and disease. A clear recording can enhance the ability of a physician to identify abnormalities and take corresponding action. This lab explored the construction of a simple analog EKG amplifier that produced relatively clean Lead I EKG recording with identifiable wave characteristics. Given the 5 bio amplifier design considerations (High Input Impedance, Electrical Isolation, Low Output Impedance, High Signal to Noise Ratio and High CMRR), as well as two other EKG design considerations (Electrode Attachment adds DC component and Contact Resistance, and Noise at 60Hz), component selection and band pass filter construction served to compensate. Results were clear enough to take amplitude and rate measurements of the resultant EKG. Later FFT analysis demonstrated that by combining a low pass filter that attenuated noise at frequencies above its cutoff, and a high pass filter that attenuated noise below its cutoff frequencies, a successful band pass filter was created to reduce noise on either side of the target frequency band, increasing SNR. Theoretical bode plots were created to verify this general behavior.

{% include pdf-embed.html url="/images/qp-physical/biological-signal-conditioning.pdf" %}
