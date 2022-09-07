---
title: "Machine Learning Practitioner's Guide"
permalink: /ml-practitioners-guide/
date: 2022-08-24T00:00-00:00
excerpt: A practitioner's guide to developing Machine Learning models that solve real problems.
toc: true
toc_sticky: true
---

> Note: As of 2022-08-29 this page is very much a WIP... currently just an outline.

This is a practitioner's guide to developing Machine Learning models that solve real problems. It focuses primarily on the processes related to deep learning models. It is meant to serve as a personal cheat-sheet/checklist and collection of snippets which I like to follow when working on ML projects.

## TLDR

- Be observant, think through problems, reflect often and remember unique problems may require novel solutions or novel combinations of existing practices.
- Machine Learning is about the overall system that facilitates learning. Think of models like lazy students. Teaching them to learn requires a well designed curriculum, appropriate facilities and opportunities for real world practice. Think through your overall system, and make sure it supports bootstrapping data, deploying a model and finding a route for feedback.
- Leverage a scientific method to derisk unknowns. Machine Learning systems require exploration, and constant consideration of what is working and what isn't. When faced with unknown properties of the system, generate a hypothesis and design an experiment. To make efficient use of time and resource, scope each experiment as small as possible to answer a specific question or derisk a specific unknown.
- Manage complexity with engineering. The systems involved get very complex and often need to adapt as you gain knowledge about the overall system. Stay agile and wrangle this complexity with solid engineering principles and design.

## Data Products vs. Decision Science

Machine Learning has become a broad term with many meanings. I find it useful to draw the distinction between what I call `Decision Science` and `Data Products`.

Decision Science

- the application of tools and techniques in pursuit of some insight - often a business insight
- this process yields an export, with results often delivered in the form of a report or dashboard
- often involves exploration of data or the modeling of some phenomenon in the data 
- may involve basic Machine Learning models (classifiers/regression) and unupervised techniques (dimensionality reduction/clustering)
- code is short lived - will not require ongoing maintenace in a production environment
- more of a focus on science, less of a focus on engineering (unless data acquisition/handling requires significant infra)

Data Products

- the development of systems which leverage learning based models to automate or facilitate intelligent function in a production environment
- this process yields a deployed system, which requires proper design and maintenance
- systems often need to be resilient, robust and adaptive to ongoing and dynamic data
- requires significant engineering effort

> This guide focuses primarily on the genre "Data Products". While many practices are applicable across genres, those curious about "Decision Science" should look for material focused on data science and analysis.

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

- what resources are available?
- search for publicly available datasets in relevant domains/problems etc.
- scrape the web
- synthetically generate data

### labeling

- bootstrapping
  - unsupervised learning/clustering + manual review
  - scripting (leverage priors/metadata/bigger models etc.)
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
- separate data code from model code... reusable data pipelines for model iteration/experimentation/evaluation/prediction/debugging/data viz etc.
- sanity check: visualize the input data at the point where it would enter the model... ie: the output of your pipeline AFTER any transformations or augmentations.

## Prototyping a model

### finding model architectures

- discovering relevant vocab/problems/datasets/industries/models etc.
- papers
- codebases
- from scratch
- tips
  - start with smallest relevant architecture (ex. res18 not res50)

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

### Feasibility Test

- before more extensive testing... build confidence in the feasibility of the approach
- constantly on the lookout for early indicators of strong signal in the data
- feasibility tests
  - Unsupervised approach
    - cluster data... looking for meaningful/well formed clusters
  - Use simple or naive feature embeddings for the data
  - If using a multi-modal model, test data modalities individually
  - Over-fit the desired model on single sample or small sample set... if it can't over-fit a single sample, there might not be enough signal in the data

### Setup for experiments

- reproducibility
  - containerize early...
  - share common code between serving + training
  - allow for easy migration/integration to cloud platforms or workflow/pipeline orchestration platforms when scaling up distributed training

- train/eval pipeline
  - artifacts should have everything required to reproduce...
  - logs and metrics
  - store model config/arguments/cli inputs etc.
  - checkpoints
  - eval visualization ... samples/cluster etc.

### Early experiments

- start with smallest architecture (ex. res18 not res50)
- early phase
  - learning rate sweep
  - generate insights...

### Determine an upper bound

- fine tune hyper-parameters manually
- avoiding perfection...
- each experiment should be intentional
- think!! hypothesize about the connection / impact of various inputs to observed behavior... reflect and re-evaluate
- depending on your resources and engineering talent, you can consider other approaches to hyper-parameter tuning
  - exhaustive -> works for tiny models/hyper-parameter spaces
  - random -> cover enough of the search space to inform further manual tuning
  - genetic/algorithmic optimization -> when compute isn't an issue, i've had success modeling a fitness function and evolving hyperparameters

### Generalize

- more data aug, generalization etc.
- early stopping
- uncertainty
- calibration
- active learning

## Model Serving

### Challenges

- train/serve skew
- sharing environment/data handling between train/serve
- usability... what to expose?

### Model versioning & storage

- ...

### Optimizations

- ...

## Explaining Performance to non-data scientists

- ...

## Last mile

- monitoring
- drift detection + explain-ability
- promoting use
- setup for success w/ non-data scientists
- vocabulary
- absolutes vs probabilities
- API design
- versioning
