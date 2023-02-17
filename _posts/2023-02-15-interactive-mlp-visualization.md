---
title: "Interactive Neural Network Visualizer"
date: 2023-02-15T00:00:00-00:00
last_modified_at: 2023-02-15T00:00:00-00:00
categories:
  - webdev
  - machine learning
  - ai
  - 3D
  - art
permalink: /post-r3f-nn-visualizer/
classes: wide
excerpt: An interactive Neural Network visualization built w/ modern web technologies including tensorflow.js and react-three-fiber.
header:
  og_image: /images/r3f-nn-visualizer/preview.webp
  teaser: /images/r3f-nn-visualizer/preview.webp
---

[![](https://github.com/dcyoung/r3f-nn-visualizer/raw/dev/docs/capture.gif){:.align-center}](https://dcyoung.github.io/r3f-nn-visualizer/)

[Click HERE for an Interactive Demo](https://dcyoung.github.io/r3f-nn-visualizer/)

[See the source code](https://github.com/dcyoung/r3f-nn-visualizer)

## Training a model

To be sure the model could run in browser on any device I turned to Tensorflow.js. I kept the setup small - an MLP w/ 2 hidden layers that learns to classify MNist digits. This should be familiar to anyone whose worked with networks.

```ts
  const model = tf.sequential();
  // Hidden Layers
  model.add(tf.layers.dense({inputShape: [28*28], units: 16, activation: "relu"}));
  model.add(tf.layers.dense({units: 16, activation: "relu"}));
  // output layer
  model.add(tf.layers.dense({units: 10, activation: "softmax"}));
```

I also added some React components to interactively kick off training/inference.

## Probing model activations

Next, I added the ability to forward a sample through the model and capture the activations from each layer. 

```ts
const probeModelActivation = async (
  sample: tf.Tensor<tf.Rank>,
  model: tf.Sequential
) => {
  // const layerInputs_BK = [tf.zeros([1, 28 * 28 * 1])];
  const layerInputs: tf.Tensor<tf.Rank>[] = [sample];
  model.layers.forEach((layer, i) => {
    const layerOutput = layer.apply(layerInputs[i]);
    layerInputs.push(layerOutput as tf.Tensor<tf.Rank>);
  });
  return new ActivationData(
    await layerInputs[0].data(),
    await Promise.all(layerInputs.slice(1).map(async (t) => await t.data()))
  );
};
```

## Visualizing Activations

Lastly, I used `react-three-fiber` to create an interactive visualization of the network including the propagation of activations. Updating a lot of 3D lines proved fairly cumbersome in `react-three-fiber`. This was unexpected as most other features in the library have been a treat. If I was starting this project over, I'd default to `GLSL` shaders to allow for bit more control.
