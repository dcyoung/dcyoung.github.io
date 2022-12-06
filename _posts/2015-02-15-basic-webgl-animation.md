---
title: "Basic 2D Animation with WebGL"
date: 2015-02-15T00:00:00-00:00
last_modified_at: 2015-02-15T00:00:00-00:00
categories:
  - webdev
  - school project
permalink: /post-webgl-animation-2d/
classes: wide
excerpt: Animating a dancing letter w/ WebGL
header:
  og_image: /images/webgl-animation/0.webp
  teaser: /images/webgl-animation/0.webp
---

<iframe
  src="/images/webgl-animation/embed.html"
  width="100%"
  style="border:none;"
  onload="(function(obj){obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';})(this)"
>
</iframe>

A basic script to animate a capital letter "I" for the fighting Illini from UIUC. The project uses javascript and WebGL to make the letter look like it is bouncing similar to the old pixar lamp. It draws the letter using 2 triangle strips with no degenerate triangles, and then animates the movements using keyframes. Prior to this I'd never worked with graphics of any kind, so this was a very basic test to get acquainted with graphics pipeline.

You can view the entirety of the commented source code here: [github.com/dcyoung/BasicWebGL_Dancing_i](https://github.com/dcyoung/BasicWebGL_Dancing_i)

The animation was broken into 4 basic positions and each was assigned a keyframe:

- pre squash
- squash
- post squash
- hover

Each keyframe is a matrix of vertex positions defining the form of the left half only for that keyframe's specific pose. Because the letter "I" is symmetrical, it was possible to use only the left half and calculate the vertex positions of the right half based off the left. A set of matrices (triangleVerticesLeftSide, and triangleVerticesRightSide) hold the current vertex position for the left and right sides of the animated letter at all times. The matrices for the keyframes simply define target positions and do not change over time.

To animate the bouncing letter, the actual vertices for the current position are updated to interpolate between different keyframe targets in the proper sequence. A library called TWEEN (short for in-between), was used to interpolate the vertex positions between different keyframes and then those tweens were chained together  in the correct order to create a looping animation. Again, because the letter is  symmetric, the tweens only interpolate values for the left half of the letter and then every time they update, a function is called to also update the right half of the letter by simply looking at the newly updated left half.
