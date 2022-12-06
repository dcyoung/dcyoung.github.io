---
title: "Generating Terrain and a simple Flight Sim w/ WebGL"
date: 2015-02-25T00:00:00-00:00
last_modified_at: 2015-02-25T00:00:00-00:00
categories:
  - webdev
  - school project
permalink: /post-webgl-terrain/
classes: wide
excerpt: Simple implementation of the diamond square algorithm to generate a tile of terrain.
header:
  og_image: /images/webgl-terrain/0.webp
  teaser: /images/webgl-terrain/0.webp
---

Simple implementation of the diamond square algorithm to generate a tile of terrain.

<iframe
  src="/images/webgl-terrain/embed.html"
  width="100%"
  style="border:none;"
  onload="(function(obj){obj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';})(this)"
>
</iframe>

You can view the entirety of the commented source code here: [github.com/dcyoung/TerrainGenerator](https://github.com/dcyoung/TerrainGenerator)

I extended this further with a very basic flight simulator created with raw WebGL. It uses quaternions for orientations: [github.com/dcyoung/FlightSimulator](https://github.com/dcyoung/FlightSimulator)
