---
title: "Modeling Neurons & Action Potentials"
date: 2013-10-11T00:00:00-00:00
last_modified_at: 2013-10-11T00:00:00-00:00
categories:
  - quantitative physiology
  - biomedical engineering
  - school project
permalink: /post-bme-modeling-neurons/
classes: wide
toc: true
excerpt: Various modeling techniques for neurons, action potentials and neuronal stimulation.
header:
  og_image: /images/qp-computational/modeling-neurons-and-action-potentials/preview.jpg
  teaser: /images/qp-computational/modeling-neurons-and-action-potentials/preview.jpg
---

![preview](/images/qp-computational/modeling-neurons-and-action-potentials/preview.jpg){:.align-right}

This page contains various modeling techniques for neurons, action potentials and neuronal stimulation. The techniques range from overly simplified to relatively intricate but still abstract the under workings to simulate the desired behavior. Other writeups exist on my site exploring these details such as modelling of ion channels themselves. The writeups in this post explore:

- Modelling both a Uni-Directional and a Bi-Directional Action Potential
- Modelling Cardiac Action Potentials
- Modelling Hodgkin and Huxley Neuronal Model using ODE45
- Dynamical Systems Approach to Neuronal Modelling
- Basic Hodgkin Huxley Neuronal Model
{:.text-justify}

## Modelling both a Uni-Directional and a Bi-Directional Action Potential

The following write up investigates the CRRSS equations in modelling a uni and a bi-directional action potential. The first problem develops a Matlab program that will solve for a propagating action potential along a 9cm axon segment. The second problem investigates an extracellular monopole source with an anodic square pulse followed by a cathodic square pulse, varying amplitudes to generate bi-directional action potentials and generating surface plots of membrane voltage as well as a video. The third problem plots various values at the instant the two action potentials have propagated halfway to each end of the axon. The fourth problem experiments with combinations of multiple anodes and cathodes as well as wave-shapes and pulse-widths to generate unidirectional propagating action potentials along the axon.

<object data="/images/qp-computational/modeling-neurons-and-action-potentials/hw4-writeup-wip.pdf" width="1000" height="1000" type="application/pdf"></object>

## Modeling Cardiac Action Potentials

This writeup studies the movement of ions in a canine ventricular myocyte using the Hund-Rudy dynamic model. The HRd model constructs the canine ventricular epicardial action potential based on the underlying ionic processes. This experiment could provide insight because many arrhythmias are manifested in abnormalities of action potential generation at the cellular level.

<object data="/images/qp-computational/modeling-neurons-and-action-potentials/clab-1-writeup-david-young.pdf" width="1000" height="1000" type="application/pdf"></object>

## Modeling Hodgkin Huxley Neuronal Model using ODE45

This writeup explores the use of ODE45 in modelling the Hodgkin-Huxley equations. 

Overview of each Problem:

1. Develops a Matlab program that will solve for membrane voltage for a given stimulus. This involves solving a system of four, coupled first order differential equations. ODE45 is used to integrate the model.
2. Assuming the resting membrane potential is -65 mV, problem 2 integrates the model until steady state membrane potential is reached (no stimulus is applied). This steady-state value of membrane voltage is then used as the new resting membrane potential and the process is repeated until the initial estimate of membrane potential matches the integrated solution. Then plots are generated of the voltage time course of the first and last model integration.
3. Using a depolarizing square pulse with duration of 0.35 ms, the magnitude of the pulse was increased until an action potential was initiated. Various plots for a typical action potential were then generated.
4. This problem explores how soon after an action potential can another action potential be initiated by the same depolarizing square pulse, as well as by much stronger pulse of triple the magnitude.
5. Use a stimulus in a hyperpolizing way, increasing the duration of the stimulus until an anode break initiation.

Upon closer inspection I believe some of my dynamics may have been off. There should not be an influx of Potassium before its efflux. Also I may have flipped the signs of the ion currents somewhere as. Na rushes in so it should be negative, while K rushes out so it should be positive.

<object data="/images/qp-computational/modeling-neurons-and-action-potentials/hw2-latex-wip.pdf" width="1000" height="1000" type="application/pdf"></object>

<object data="/images/qp-computational/modeling-neurons-and-action-potentials/writeup.pdf" width="1000" height="1000" type="application/pdf"></object>

## Dynamical Systems Approach to Neuronal Modeling

<object data="/images/qp-computational/modeling-neurons-and-action-potentials/dynamical-systems-approach-to-neuron-modelling.pdf" width="1000" height="1000" type="application/pdf"></object>

## Hodgkin Huxley Neuronal Model

<object data="/images/qp-computational/modeling-neurons-and-action-potentials/hodgkin-huxley.pdf" width="1000" height="1000" type="application/pdf"></object>
