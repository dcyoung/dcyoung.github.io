---
title: "Machine Learning Cookbook"
permalink: /cookbook/
date: 2022-08-24T00:00-00:00
excerpt: A practioner's guide to developing Machine Learning models that solve real problems.
toc: true
toc_sticky: true
---

This is a practioner's guide to developing Machine Learning models that solve real problems. It has evolved over the years from a personal cheatsheet and collection of snippets.

## Cheatsheet

- Exploration
  - visualize + profile data
- Scope
  - define problem
  - where does model fit...
  - how will it be used
  - overall system
  - cascade effects etc.
  - consider availability of feedback/qa/validation/ground truth etc.
- consider easier/alternative/explicit options
- unsupervised learning
- labeling
- dataset organization
  - separate datums from annotations/structure/labels etc.
  - treat like a database
  - build interfaces and adapters in code
- data pipeline
- data augmentation
- separate data code from model code... reusable data pipelines for model iteration/experimentation
- finding model architectures
  - discovering relevant vocab/problems/datasets/industries/models etc.
  - papers
  - codebases
  - from scratch
- feasability
  - overfit model on single sample or small sample set
- reproducability
  - containerize early...
  - share common code between serving + training
- train/eval pipeline
  - artifacts should have everything required to reproduce...
  - logs and metrics
  - store model config/arugments/cli inputs etc.
  - checkpoints
  - eval visualization ... samples/cluster etc.
- early indicators
  - learning rate sweep
  - insights...
- determine upper bound
  - fine tune hyper-parameters manually
  - fine tune hyper-parameters exhaustive
  - avoiding perfection...
  - think!! hypothesize about the connection / impact of various inputs to observed behavior... reflect and re-evaluate
- generalization
  - data aug, generalization etc.
  - early stopping
  - uncertainty
  - calibration
  - active learning

## TODO

todo...
