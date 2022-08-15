---
title: "Custom Racing Simulator Rig"
date: 2015-03-01T00:00:00-00:00
last_modified_at: 2015-03-01T00:00:00-00:00
categories:
  - diy
  - automotive
  - motorsports
  - electronics
permalink: /post-racing-simulator-rig/
classes: wide
toc: true
excerpt: Building a custom racing simulator with a direct drive wheel and hydraulic handbrake.
header:
  og_image: /images/racing-simulator/pedals/0.jpg
  teaser: /images/racing-simulator/pedals/0.jpg
---

<figure class="half">
    <img src="/images/racing-simulator/pedals/0.jpg">
    <img src="/images/racing-simulator/pedals/1.jpg">
</figure>

I built a simulator years ago for sims like Rfactor, Richard Burns Rally and iRacing. Back then triple screens were the most immersive option. Unfortunately I ended up selling my original rig to fund other projects, but always missed it. When I started playing with VR headsets I knew I had to build another.

I decided to build something that was adjustable enough to support future modifications (like motion) with hardware that would support a high torque direct drive wheel and realistic input forces for pedals, shifters and handbrake.

## 80/20 Frame + Cheap Bucket Seat

80/20 is a type of aluminum extruded tubing with t-nut slots that permit all manner of brackets to be mounted. The material is very easy to work and extremely rigid. Its like working with giant erector set/tinker toys. The actual aluminum is decently priced, but all the hardware is insanely overpriced, so I sourced a supplier who modified the tubing to fit together with standard hardware instead. This ended up being the cheapest route and he even cut the pieces i requested to length.

<figure class="half">
    <img src="/images/racing-simulator/chassis/0.jpg">
    <img src="/images/racing-simulator/chassis/1.jpg">
</figure>

Dry fitting it all together...

<figure class="third">
    <img src="/images/racing-simulator/chassis/2.jpg">
    <img src="/images/racing-simulator/chassis/3.jpg">
    <img src="/images/racing-simulator/chassis/4.jpg">
</figure>
<figure class="half">
    <img src="/images/racing-simulator/chassis/6.jpg">
    <img src="/images/racing-simulator/chassis/8.jpg">
</figure>
<figure class="half">
    <img src="/images/racing-simulator/chassis/5.jpg">
    <img src="/images/racing-simulator/chassis/7.jpg">
</figure>

The knockoff racing seat had mounting holes that weren't quite symmetrical. I had to whip up some brackets for that as well.

![12.jpg](/images/racing-simulator/chassis/12.jpg){:.align-center}

<figure class="third">
    <img src="/images/racing-simulator/chassis/9.jpg">
    <img src="/images/racing-simulator/chassis/10.jpg">
    <img src="/images/racing-simulator/chassis/11.jpg">
</figure>


## Direct Drive Force Feedback Wheel

Major Parts list:

- Simucube Servo Drive
- 480 Watt Power Supply
- MIGE 130ST-M10010 servo motor  (a.k.a: "small mige") w/ 5000 ppr encoder
- Motor shaft to steering wheel adapter
- Adjustable motor mount
- Motor cables w/ DB15 Connectors & Ferrite Cores
- Emergency Stop button

​Assembling the SimuCube...

<figure class="half">
    <img src="/images/racing-simulator/wheel/0.jpg">
    <img src="/images/racing-simulator/wheel/2.jpg">
</figure>

<figure class="third">
    <img src="/images/racing-simulator/wheel/3.jpg">
    <img src="/images/racing-simulator/wheel/4.jpg">
    <img src="/images/racing-simulator/wheel/5.jpg">
</figure>

## Pedals

For maximum adjust-ability I opted for the ProtoSimtech PT-1 pedals. The brake pedal may use a load cell rather than a full hydraulic setup, but its still a top tier pedal set at a mid tier price in my opinion. The  ability to mount each pedal direct to the 80/20 means the spacing of pedals can be setup exactly how I like it for left-foot braking and/or heel-toe. I went for an inverse mount as well.

<figure class="half">
    <img src="/images/racing-simulator/pedals/0.jpg">
    <img src="/images/racing-simulator/pedals/1.jpg">
</figure>

## Shifter

I opted to go with Derek-Speare's sequential shifter. The one pictured next to the packaging is the straight shaft, but that was a shipping mixup and I've since acquired a shifter with an angled shaft (mounted to the rig).

<figure class="third">
    <img src="/images/racing-simulator/shifter/0.jpg">
    <img src="/images/racing-simulator/shifter/1.jpg">
    <img src="/images/racing-simulator/shifter/2.jpg">
</figure>

## Analog Hydraulic Handbrake

This was a little project in and of itself. I wanted a realistic feeling handbrake, as I really enjoy rally sims. So I made a hydraulic handbrake the same way I would for a drift or rally car. Instead of a caliper though, I just used a pull type slave cylinder that compresses some bushings. A pressure transducer provides an analog reading which is converted to a digital input for the computer.

### Parts

<figure class="third">
    <img src="/images/racing-simulator/handbrake/0.jpg">
    <img src="/images/racing-simulator/handbrake/1.jpg">
    <img src="/images/racing-simulator/handbrake/2.jpg">
</figure>

<figure class="third">
    <img src="/images/racing-simulator/handbrake/3.jpg">
    <img src="/images/racing-simulator/handbrake/4.jpg">
    <img src="/images/racing-simulator/handbrake/5.jpg">
</figure>

### Layout

<figure class="third">
    <img src="/images/racing-simulator/handbrake/6.jpg">
    <img src="/images/racing-simulator/handbrake/7.jpg">
    <img src="/images/racing-simulator/handbrake/8.jpg">
</figure>

### Fitting Bushing to slave cylinder

The slave cylinder is a pull type, so the resistance is provided by common skateboard bushing which are compressd under load.

<figure class="third">
    <img src="/images/racing-simulator/handbrake/9.jpg">
    <img src="/images/racing-simulator/handbrake/10.jpg">
    <img src="/images/racing-simulator/handbrake/11.jpg">
</figure>

### Mounting

Given that the handbrake is hydraulic and the lever arm is rather long, the base needed to be mounted to something stout. I also wanted wanted to keep the master cylinder as low as possible to avoid any kind of creative reservoir mounting, which meant angling the base of the handbrake. First I mocked up the angle I wanted using some clamps and aluminum plate. Then I created an extra support arm from 1.5" aluminum tubing that had an angled beam on which to mount the aluminum plate, and subsequently the handbrake. The result is incredibly strong also adds extra support to the chassis of the rig.

<figure class="third">
    <img src="/images/racing-simulator/handbrake/12.jpg">
    <img src="/images/racing-simulator/handbrake/13.jpg">
    <img src="/images/racing-simulator/handbrake/14.jpg">
</figure>

<figure class="third">
    <img src="/images/racing-simulator/handbrake/15.jpg">
    <img src="/images/racing-simulator/handbrake/17.jpg">
    <img src="/images/racing-simulator/handbrake/18.jpg">
</figure>

To keep elbow room when sitting in the rig, I chose to remote mount the reservoir with the help of slick angled AN to hose-barb fitting. I routed the tubing through the support arm and mounted the slave cylinder underneath the plate. The slave cylinder can basically hang without any intense mounting, as it pulls on itself and does not require any opposition from mounting.

<figure class="half">
    <img src="/images/racing-simulator/handbrake/19.jpg">
    <img src="/images/racing-simulator/handbrake/20.jpg">
</figure>

<figure class="half">
    <img src="/images/racing-simulator/handbrake/21.jpg">
    <img src="/images/racing-simulator/handbrake/23.jpg">
</figure>

<figure class="half">
    <img src="/images/racing-simulator/handbrake/22.jpg">
    <img src="/images/racing-simulator/handbrake/24.jpg">
</figure>

## Software Control

More to come on this... its a never ending task with endless parameter tuning and testing.

## Motion System (Rear Traction Loss)

First addition... coming soon :)