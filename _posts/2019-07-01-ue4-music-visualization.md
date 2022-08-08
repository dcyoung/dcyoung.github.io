---
title: "Interactive Music Visualization in Unreal Engine"
date: 2019-07-01T00:00:00-00:00
last_modified_at: 2019-07-01T00:00:00-00:00
categories:
  - audio visualization
  - 3D
  - art
  - unreal engine
permalink: /post-ue4-music-visualization/
classes: wide
excerpt: Early experiments creating interactive AV tools enabling a user to play with sound in a 3D context.
---

<!-- [![Video](https://yt-embed.herokuapp.com/embed?v=pBBv5oWQoYE){:.align-center}](https://www.youtube.com/watch?v=pBBv5oWQoYE "Video") -->
<div class="video-wrap" style="width:100%; max-width: 600px; margin: auto;">
    <div class="video-container" style="position: relative; overflow: hidden; height: 0; padding-bottom: 56.25%; text-align: center;">
        <iframe src="https://www.youtube.com/embed/pBBv5oWQoYE" title="YouTube video player"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; max-width: 100%;" frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen></iframe>
    </div>
</div>

## Analyzing Audio

In order to visualize audio, it must first be processed into a format more conducive to visualization. Broadly this is the field of digital signal processing. I started this project by writing a custom DSP library for UE4 which relied on the FMOD - borrowing inspiration from [parallelcube](www.parallelcube.com/2018/03/01/using-thirdparty-libraries-in-our-ue4-mobile-project/).

This worked for a basic frequency analyzer!

However, after some experimentation, FMOD proved to be an "all in" kind of solution to audio analysis, and I was after something a bit more flexible. I later switched from using my custom DSP library, to using an existing audio analysis plugin, mostly for the ability to process external audio streams (ie: PC audio) rather an imported file. This allowed me to focus effort on the visualizations.

## Visualizing Frequency Spectrum

I started by creating a ReactiveVisualizer interface and a manager which pipes the audio analysis to any implementations that exist in the scene. The first implementation was a simple exercise in moving from familiar frequency spectrum visualizations to actual 3D geometry. A procedurally generated row of cubes corresponds to various frequency ranges. Each cube grows in size based on the intensity/amplitude of the corresponding frequency. I extended these principles to 2D and spherical coordinates as well.

row | grid | spherical
:-------------------------:|:-------------------------:|:-------------------------:
[![freq-1d](https://yt-embed.herokuapp.com/embed?v=Vc32w8Er-L0)](https://www.youtube.com/watch?v=Vc32w8Er-L0 "freq-1d") | [![freq-2d](https://yt-embed.herokuapp.com/embed?v=cBzsFvg_5VI)](https://www.youtube.com/watch?v=cBzsFvg_5VI "freq-2d")| [![spherical](https://yt-embed.herokuapp.com/embed?v=QBhdw1tvAQM)](https://www.youtube.com/watch?v=QBhdw1tvAQM "spherical")

Details include:

- Procedurally generated grid
- Instanced static meshes for performance
- Can be modified in real-time
- Implemented various interpolation methods to yield smoother, or more pixelated visuals
- Grid visualization styles (row, col, radial, inverse radial etc.)
- Spherical visualization styles (fibonacci sphere index, equator & inv, latitude & inv, longitude & inv, lat+long & inv)

## Adding Interaction

The goal is interactivity, and up until now all these visuals have been **reactive** but not **interactive**. I started with a simple experiment where the intensity/behavior of a reactive visualizer is influenced by the proximity of a target object.

<!-- [![Interactive](https://yt-embed.herokuapp.com/embed?v=OxsfofZAA40){:.align-center}](https://www.youtube.com/watch?v=OxsfofZAA40 "Interactive") -->

<div class="video-wrap" style="width:100%; max-width: 600px; margin: auto;">
    <div class="video-container" style="position: relative; overflow: hidden; height: 0; padding-bottom: 56.25%; text-align: center;">
        <iframe src="https://www.youtube.com/embed/OxsfofZAA40" title="YouTube video player"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; max-width: 100%;" frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen></iframe>
    </div>
</div>


I then extended this experiment by using the proximity of tracked hand controllers to control the behavior/intensity of the reactive visualizer. Unfortunately I don't have a video as desktop capture in VR is wonky. It was cool though - trust me!

## Adding dimensions to medium, Playing Video

I was playing around with video textures for another project (interactive cloth simulation), and thought it would be fun to try adding a dimension to what is traditionally a very 2D medium (video).

<!-- [![Video](https://yt-embed.herokuapp.com/embed?v=pBBv5oWQoYE){:.align-center}](https://www.youtube.com/watch?v=pBBv5oWQoYE "Video") -->

<div class="video-wrap" style="width:100%; max-width: 800px; margin: auto;">
    <div class="video-container" style="position: relative; overflow: hidden; height: 0; padding-bottom: 56.25%; text-align: center;">
        <iframe src="https://www.youtube.com/embed/pBBv5oWQoYE" title="YouTube video player"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; max-width: 100%;" frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen></iframe>
    </div>
</div>
