---
title: "Automatic Secret Knock-Detecting Door Opener"
date: 2014-03-01T00:00:00-00:00
last_modified_at: 2014-03-01T00:00:00-00:00
categories:
  - electronics
  - diy
permalink: /post-secret-knock-detector/
classes: wide
excerpt: Tap a secret knock and a real door opens.
header:
  og_image: /images/secret-knock-detector/banner.jpg
  teaser: /images/secret-knock-detector/banner.jpg
---

![banner](/images/secret-knock-detector/banner.jpg){:.align-center}

A few secret knock detecting Arduino projects exist around the web, meaning the basic micro-controller logic for the knock sensing function has been fleshed out. With confidence that the software end would work, I set out to build a secret knock detecting door opener that would open my door if provided a secret knock.

​My original plan was to interface with the electric deadbolt in my apartment door, but upon inspection the unit is upwards of **$900** and I'd prefer not to take any chances messing with the internals. A bit less elegant is a mechanical system that would open the door by the door handle itself. Since the project requires no finesse or accuracy in motor control, I figured a cheap high torque servo motor flipped through a pulley would likely do the trick. An MG995 13Kg-cm high torque servo costs about **$6-7** and can be modified for full rotation. I designed a custom winch system to pull the door knob open.

Because the Arduino handles all the analysis and control, the circuit is relatively simple. I've sketched it below. A variable potentiometer allows the sensitivity to be adjusted and the LEDs indicate success or failure of the knock for debugging purposes. I constructed an arduino shield with the same circuit.

Lastly, I constructed a winch from an MG955 servo (modified for continuous rotation), a custom servo winch drum and common wire for hanging picture frames.

<figure class="third">
  <img src="/images/secret-knock-detector/circuit.jpg">
  <img src="/images/secret-knock-detector/prototype.jpg">
  <img src="/images/secret-knock-detector/winch.jpg">
  <figcaption>Circuit (left), arduino shield (middle), winch (right)</figcaption>
</figure>
