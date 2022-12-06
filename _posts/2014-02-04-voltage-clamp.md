---
title: "Voltage Clamp"
date: 2014-02-04T00:00:00-00:00
last_modified_at: 2014-02-04T00:00:00-00:00
categories:
  - quantitative physiology
  - biomedical engineering
  - school project
permalink: /post-bme-voltage-clamp/
classes: wide
excerpt:  Constructing a circuit to study the behavior of a voltage clamp.
header:
  og_image: /images/qp-physical/voltage-clamp.webp
  teaser: /images/qp-physical/voltage-clamp.webp
---

## Abstract

A circuit was constructed to simulate the action of a voltage clamp. The circuit low pass filtered the membrane potential, compared it to the control voltage, amplified the difference by the gain and by that feedback, injected current to compensate. The response of the circuit to various experimental conditions facilitated an understanding of the contributions of individual components, as well as the physiological significance of each. By controlling the value of a variable resistor (Rg), the circuit's steady state response was analyzed for varying gain values and it was determined that larger gain produced smaller deviations between Vm and Vc. Similar studies for Rm showed that small Rm values produced large deviations between Vm and Vc. Comparing rising time constants, for the response and the control,demonstrated the effect on dynamic response resulting from changing parameters. An analysis of bode magnitude plots for various gain values visually demonstrated the low pass filter behavior of the voltage clamp. Sources of error resulted in a few outlying data points, making the experimental results slightly mixed. A hypothetical analysis of each experiment made clearer the trend that was still evident, but clouded, in the experimental data.

## Writeup

{% include pdf-embed.html url="/images/qp-physical/voltage-clamp.pdf" %}
