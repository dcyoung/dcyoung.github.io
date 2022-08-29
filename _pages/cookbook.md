---
title: "Machine Learning Practioner's Guide"
permalink: /ml-practioners-guide/
date: 2022-08-24T00:00-00:00
excerpt: A practioner's guide to developing Machine Learning models that solve real problems.
toc: true
toc_sticky: true
---

> Note: This guide is very much a WIP... currently an outline as of 2022-08-29

This is a practioner's guide to developing Machine Learning models that solve real problems. It is meant to serve as a personal cheatsheet/checklist and collection of snippets I like to follow when working on ML projects.

## Know the Lifecycle

- Decision Science vs. Data Products
- Analysis vs. Models
- Reports vs. Deployment

## Dedicate time to Explore

- Gather small but representative distribution of data from domain
- Explore the data...
  - visualize
  - profile
  - ML for exploration
    - clustering
    - unsupervised learning

## Scope your project

- Define the problem
- Does this problem really need a learning based solution?
  - consider easier/alternative/explicit options
- Model is part of an ecosystem
  - overall system design?
  - where does model fit
  - how will it be used
  - cascade effects etc.
  - consider availability of feedback/qa/validation/ground truth etc.

## Gather Data

### get creative sourcing data
- what resources are avaialble?
- search for publically available dataets in relevant domains/problems etc.
- scrape the web
- synthetically generate data

### labeling
- bootstrapping
  - unsupervised learning/clustering + manual review
  - scripting (leverage priors/metadata etc.)
  - get hands dirty labeling...
    - existing tooling
    - custom tooling

### dataset organization tips
- you'll likely spend more time dealing with data than with models... 
- design for extensibility/maintenance/ease of use
- separate datums from annotations/structure/labels etc.
  - you'll often iterate on annotation or data formats meaning which can be slowed down by static datasets or tight coupling
- treat like a database
- build interfaces and adapters in code

### Build a working data-pipeline early

- data pipeline
- data augmentation
- separate data code from model code... reusable data pipelines for model iteration/experimentation

## Prototyping a model

### finding model architectures
- discovering relevant vocab/problems/datasets/industries/models etc.
- papers
- codebases
- from scratch

### project structure

- The use of models is often blocked by a disconnect between data science and engineering. To combat this, it is best to incorporate solid software engineering practices as soon as a project moves beyond exploration or spike experiments.
- Benefits of a modular structure 
  - codebase navigation/interpretability/maintenance/refactoring etc.
  - easier experiments, extension/adaptation
  - promotes code/module reuse
  - combats train/serve skew by sharing as much environment/code as possible
  - collaboration
- As a rough outline, most deep learning projects typically include the following modules 
  - IO
  - dataset handling
  - augmentation pipelines
  - model configuration
  - model definition
  - training configuration
  - evaluation utilities
  - scripts...
    - train/eval/predict
    - also lots of visualization + exploratory

## Training

### Feasability Test

- before more extensive testing... build confidence in the feasbility of the approach
- constantly on the lookout for early indicators of strong signal in the data
- feasability tests
  - Unsupervised approach
    - cluster data... looking for meaningful/well formed clusters
  - Use simple or naive feature embeddings for the data
  - Overfit the desired model on single sample or small sample set... if it can't overfit a single sample, there might not be enough signal in the data

### Setup for experiments

- reproducability
  - containerize early...
  - share common code between serving + training
  - allow for easy migration/integration to cloud platforms or workflow/pipeline orchestration platforms when scaling up distributed training

- train/eval pipeline
  - artifacts should have everything required to reproduce...
  - logs and metrics
  - store model config/arugments/cli inputs etc.
  - checkpoints
  - eval visualization ... samples/cluster etc.

### Early experiments

- early phase
  - learning rate sweep
  - generate insights...

### Determine an upper bound

- fine tune hyper-parameters manually
- fine tune hyper-parameters exhaustive
- avoiding perfection...
- each experiment should be intentional
- think!! hypothesize about the connection / impact of various inputs to observed behavior... reflect and re-evaluate

### Generalize

- more data aug, generalization etc.
- early stopping
- uncertainty
- calibration
- active learning

## Model Serving

### Challenges

- train/serve skew
- sharing environemnt/data handling between train/serve
- usability... what to expose?
 
### Model versioning & storage
- ...

### Optimzations
- ...

## Explaining Performance to non-data scientists

- ...

## Setup for success w/ non-data scientists

- vocabulary
- absolutes vs probabilities
- API design
- versioning 
