---
title: "Multiplayer Networked Game of Set"
date: 2014-05-01T00:00:00-00:00
last_modified_at: 2014-05-01T00:00:00-00:00
categories:
  - game dev
  - school project
permalink: /post-multiplayer-networked-game-of-set/
classes: wide
excerpt: A completely custom networked implementation of a card game called set.
header:
  og_image: http://img.youtube.com/vi/RxnU3vh2yr0/0.jpg
  teaser: http://img.youtube.com/vi/RxnU3vh2yr0/0.jpg
---

{% include video id="RxnU3vh2yr0" provider="youtube" %}

For a networking and concurrency class I was tasked with creating a simple game that connected clients over a server.  Although the intended result was expected to be a swing gui with a few click buttons, I decided to stretch the boundaries a little and implement a more complex  gui framework and a more capable back end for the networking.  This ended up being a great exercise in gui's, server and client communication as well as concurrency with some reliability tricks like blocking queues,

See the source code [here](https://bitbucket.org/dcyoung/networked-game-of-set/src/60d05d3569a42f1119684c71e4cce231a5fea791?at=master)
