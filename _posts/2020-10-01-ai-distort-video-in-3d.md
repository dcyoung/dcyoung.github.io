---
title: "Using AI to add dimensions to video"
date: 2021-10-01T00:00:00-00:00
last_modified_at: 2021-10-01T00:00:00-00:00
categories:
  - ai
  - 3D
  - unreal engine
  - art
permalink: /post-using-ai-to-add-dimensions-to-video/
classes: wide
excerpt: Experiments adding dimension to video footage, using simple and AI driven approaches.
header:
---

Previous experiments messing with video textures were so successful that I'm eager to see if the 3D effects can be used to target more semantically meaningful content in a video -- that is, to drive video effects with a perceptual understanding of the content in the video. This experiment segments dancers in the video and applies depth effects to the geometry selectively. This is accomplished entirely inside the shader, and the 3D grid is a single mesh.

segmentation test #1             |  segmentation test #2
:-------------------------:|:-------------------------:
[![Segmentation Test #1](https://img.youtube.com/vi/55A24omqleM/hqdefault.jpg)](https://www.youtube.com/watch?v=55A24omqleM "Segmentation Test #1") |  [![Segmentation Test #2](https://img.youtube.com/vi/PkeDwmLdZPk/hqdefault.jpg)](https://www.youtube.com/watch?v=PkeDwmLdZPk "Segmentation Test #2")

In the experiment above (ipod commercial), the effect is driven by a simple color threshold... which is far from a semantic understanding of the content. So to follow up, I decided to distort the 3D geometry of a mesh based on the content of a video, as interpreted by an artificial neural network. The rough process is as follows:
​
1. Create masks for each frame of video using an Instance Segmentation Network trained to segment people from images. Funny enough...  this was easiest and quickest part of the experiment by far.
2. Create 2 synchronized videos (1 original, 1 mask) and media textures for each
3. Create a procedural grid mesh with vertices linked to the the 2 media textures through UVs
4. Color vertices of the mesh by sampling the media texture for the original video
5. Offset vertex positions by sampling the media texture for the mask video

While the end result isn't as exciting or visually pleasing as past explorations, I enjoyed incorporating aspects of AI and computer vision to drive the visual effects. I think this could be used to drive more subtle effects (particles, distortions etc) in something like a music video or hyper stylized film.

[![Connecting Instruments to Unreal Engine](https://yt-embed.herokuapp.com/embed?v=zAM2T98uUm8){:.align-center}](https://www.youtube.com/watch?v=zAM2T98uUm8 "Using AI to Distort Videos in 3D")
