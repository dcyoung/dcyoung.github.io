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
- Machine Learning is about the **overall system** that facilitates learning. Think of models like lazy students. Teaching them to learn requires a well designed curriculum, appropriate facilities and opportunities for real world practice. Think through your overall system, and make sure it supports bootstrapping data, deploying a model and finding a route for feedback.
- Balance the development and focus across the big 3: `Data`, `Compute` and `Algorithms/Model Architecture`.
- Leverage a scientific method to derisk unknowns. Machine Learning systems require exploration, and constant consideration of what is working and what isn't. When faced with unknown properties of the system, generate a hypothesis and design an experiment. To make efficient use of time and resource, scope each experiment as small as possible to answer a specific question or derisk a specific unknown.
- Manage complexity with engineering. The systems involved get very complex and often need to adapt as you gain knowledge about the overall system. Stay agile and wrangle this complexity with solid engineering principles and design.

## Data Products vs. Decision Science

Machine Learning has become a broad term with many meanings. I find it useful to draw the distinction between what I call `Decision Science` and `Data Products`.

`Decision Science` is the the application of tools and techniques in pursuit of some insight - often a business insight. This process yields an export, with results often delivered in the form of a report or dashboard. Decision science involves exploration of data or the modeling of some phenomenon in the data, which may or may not involve basic Machine Learning models (classifiers/regression) and unsupervised techniques (dimensionality reduction/clustering). Code is typically short lived, in that it will not require ongoing maintenance in a production environment. Here there is more of a focus on science, and less of a focus on engineering - unless data acquisition/handling requires significant infra.

![0](/images/ml-guide/decision-science.svg){: .align-center}

`Data Products` on the other hand, represent the development of systems which leverage learning based models to automate or facilitate intelligent function in a production environment. The process yields a deployed system, which requires proper design and maintenance. Systems often need to be resilient, robust and adaptive to ongoing and dynamic data. Therefore, they live or die by the quality of feedback mechanisms, and requires significantly more engineering effort.

![0](/images/ml-guide/data-product.svg){: .align-center}

> This guide focuses primarily on the genre "Data Products". While many practices are applicable across genres, those curious about "Decision Science" should look for material focused on data science and analysis.

## The Big 3

The best results come from projects that balance the big 3:

- Data
- Compute
- Algorithms/Model Architecture

Each is an area warranting focused research or engineering - however, succesful systems will balance the development of all three for the best results.

![0](/images/ml-guide/tiangle.svg){: .align-center}

Think of these components like legs of a telescoping tripod and devote time to each in a balanced way.

## Models simplify the complexity of raw data

Models don't make decisions and they don't take actions.

Rather, models are used to increase decision making power. They inform other parts of a system which actually take actions or apply business logic. A model won't update a database, email a user or rotate a steering wheel. Instead, there exists a more traditional software layer which considers the output of a model when deciding what action to take.

One interpretation is that the model is "simplifying" the complexities of raw data to better inform critical decisions or actions.

![0](/images/ml-guide/simplify-data.svg){: .align-center}

> A predictive model maps raw data into a format that supports making the critical decision

Understanding this functional role of a model helps in the early/design phases of an ML project. If you cannot clearly articulate how this applies to your system then you are at risk of wasting cycles gathering irrelevant data or training models with irrelevant outputs.

## Finding Functional Boundaries for Preditive Models

Assuming your data is complex enough to warrant a predictive model, you'll need to define the input/output (IO) of the model. You'll likely want to jump right to model architectures - but DON'T. The functional boundaries for your model will depend on the qualities of your data and system design. So at this stage, **pretend the model is a black box and spend time understanding your data and the objectives of the overall system.**

Take a mixed approach by breaking this process into into two activites: **system analysis** and **data exploration**.

**Part 1: System Analysis**

This is about understanding the overall system as a whole and identifying the constraints that will shape the boundaries of the model. Here is a rough exercise:

1. Define and articulate a clear objective of the overall system - the desired action or outcome

2. Determine the minimal information - data simplicity threshold - to support that objective. If it helps, think of this as a question you'd ask a hypothetical human expert. As an exaggerated exercise, think of what magical insight could simplify your application logic like so:

```python
if magical_insight(raw_data):
  # take action
```

3. Think through what raw data could be relevant or help produce that magical insight

4. Study your system to identify any opportuities for automated feedback loops. Are there any existing or planned parts of a system which present opportunities to collect data samples or labels in production? Model IO that is closer to the IO of existing system components will facilitate rapid boostrapping of datasets and automated model improvement.

**Part 2: Exploration**

Part 1 stressed the importance of analyzing the overall system to identify guiding constraints for the model IO. Equally important is dedicating time to **explore your data** and better understand the domain of your problem and data. You cannot reason accurately about data you've never seen. You need to build a gut intuition about what is relevant, and how to separate signal from noise.

1. First, **gather small but representative distribution of data** from the domain.

2. **Explore without software**. Try to understand and poke at the data without software or tools. What does it looks like... if relevant, investigate how subject matter experts solve this without software.

3. **Identify strong signal** among the features in the data. Put on a data science hat, and explore using tools. Try to find early indicators or features in the data that should lend well to training a model. Not only will this help guide model inputs later, it also builds confidence that a learning apporach will work at all... which is important early on. This phase includes `data visualization`, `data profiling`, and even ML for exploration (`clustering`, `unsupervsied learning`).

4. Brainstorm strategies to boostrap a labeled dataset. Think through which parts of the data can be sourced, synthetically generated, augmented etc.

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
  - The format of data and annotations can change over the course of a project. It is easier to iterate if you avoid tight coupling between the datums and the annotations.
  - treat like a database -- the relationships that define the dataset should be loadable/dynamic/queryable -- even if that is inferred from the structure of a directory on a local file system to start.
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

### Handling Uncertainty

- in real world decision making, modeling and communicating uncertainty is often more important than accuracy
  - handling mistakes (false positives) can be more costly than flagging anomalies and forcing intervention
  - system design should include mechanisms for QA/intervention/fallback/decision overrides etc.
  - unlike traditional software development - which focuses on creating a "bug free" system - in practice, ML is never bug free and it is safer to design systems that leverage uncertainty to handle bugs with appropriate mechanisms or strategies.
- common pitfalls
  - overemphasizing accuracy
  - waiting until deploy time to consider and understand out of distribution data
  - interpreting softmax scores as confidence/uncertainty
- types of uncertainty
  - aleatoric vs. epistemic
- techniques for modeling uncertainty...
  - aleatoric: modeling distribution of data (ie: probability of data taking form of prediction)
  - epistemic: Bayesian -> modeling network uncertainty with probablistic paramters, Consensus -> modeling network uncertainty with ensembles/monte carlo dropout etc.
- out of distribution detection
- quick tricks...

## Model Serving

### Challenges

- combating train/serve skew
- incorporating data pre/post processing
- making predictions intuitive and usable... what do you expose?
- defining boundaries... where do you put business logic?
- sharing the environment + data handling across both training and inference
- estimating and managing load
- scaling
- monitoring performance
- communicating performance (key metrics?)
- optimizing throughput & latency

### Define your inference needs

Typically, low latency and high throughput come w/ added complexity - so start simple and really understand your performance needs. Start by thinking through the expected usage pattern for your inference problem.

- realtime, scheduled, offline?
- what does a client look like? (environment/service/app/programming language etc.)
- how many clients will be making requests? how often?
- what matters in your scenario - latency, throughput or both?
- is the scenario batch-able
```python
output_a = request_model_pred(input_a)
output_b = request_model_pred(input_b)
```
- is there a sequential nature to your pipeline...
```python
output_a = request_model_a_pred(input_data)
output_b = request_model_b_pred(output_a)
```
- do you need to persist raw model outputs (logging, metrics, downstream processing etc.)
- how frequently is the model updating?

### Version Control for ML

- Model versioning and storage
  - Model weights
  - Model config
  - Training config to reproduce?
  - Dataset to reproduce?
- Data versioning and storage
- Experiment tracking & reproducability
- Data pre/post processing?
- Don't think of versioning a model... think of versioning the entire "Inference System"
- prioritize a version control for the "inference system" as a whole, and find a way to make sure the "models" are released in lockstep with the data handling (pre/post processing) involved in the inference pipeline. In cloud or kubernetes environments, this can look like a "chart" version" (think helm or kustomize).
- For the actual storage of models, I prefer not to add intermediate stores and instead make it easy to reference the exact "experiment or code" that produced the model.
- For projects that aim to automate a closed loop system, traceability and programmatic references between data/training/deployment become crucial.
-  If you're in a cloud environment (or docker-compose on LFS) you can use init-containers to download model artifacts and make them available to the serving container using volumes. This simplifies the responsibilities of your model server at the cost of orchestration, allowing for arbitrary logic in the versioning and handling of models.

### Tiers of Complexity

- ...

### Train Serve Skew

- ...

![0](/images/ml-guide/train-serve-skew.svg){: .align-center}


![0](/images/ml-guide/share-data-processing.svg){: .align-center}

### Optimizations

- distributed systems
- centralizing model inference
- parallelization strategies
- optimized models
  - pruning
  - TensorRT
  - mixed precision
- optimized model servers (triton/tf-serving etc.)
  - TensorRT
  - server side batching
  - MKL optimized CPU variants
  - GPU model sharing
- ...

## QA & Feedback Mechanisms

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
