---
title: "Custom Beer Pong Tables"
date: 2014-04-01T00:00:00-00:00
last_modified_at: 2014-04-01T00:00:00-00:00
categories:
  - electronics
  - diy
permalink: /post-beer-pong-table/
classes: wide
excerpt: Building a custom beer pong table with audio reactive lighting.
header:
  og_image: http://img.youtube.com/vi/ulqUuxT_21k/0.jpg
  teaser: http://img.youtube.com/vi/ulqUuxT_21k/0.jpg
---

{% include video id="ulqUuxT_21k" provider="youtube" %}

I've always enjoyed building things, but rarely get to share my creations. The obvious solution is to choose a project that's intrinsically designed for a party. So the custom beer pong tables were born. While I don't really care that much for beer pong myself, I have enjoyed building tables. They started off simple but as always when finishing up a project, there's a strong itch to build a better version with new ideas. Although the first tables were just sturdy carpentry projects, 2 tables were taken a step further to party greatness, which I dubbed v1.0, and v2.0.    

---

## Table v1.0

I designed the first table to be portable, fold-able and lightweight. Decorating the table was accomplished with black lights and fluorescent paint. But the glowing effects didn't cut it... v2.0 needed some powered electrical light sources.

![v1](/images/beer-pong-table/v1.webp){:.align-center}

## Table v2.0

v2.0 was meant to be an exercise in electrical engineering. The design was ambitious and inspired by quite a few electrical projects floating around the web. One open source project in particular really made this possible.

Specs:

- Automatic ball washers
- Center LED matrix/grid
- Bluetooth connectivity
- Frequency spectrum analyzer synced with music being played on a laptop displayed on the center matrix.
- Scrolling Text Display
- Photoresistor triggered LED rings around the cups.

### Building the Physical Table (Wood Work)

The new table requires a lot of electronic components. The table is to be subjected to rowdy party goers, potential party fouls and spilled beverages. This means that to properly house all these components a more substantial frame had to be constructed. I opted to use wood materials again, but witnessing some significant warping in the first table I chose to use heavy duty ply and build a more rigid frame.

**Constructing the Frame Rails**

<figure class="third">
  <img src="/images/beer-pong-table/frame_rails/0.webp">
  <img src="/images/beer-pong-table/frame_rails/1.webp">
  <img src="/images/beer-pong-table/frame_rails/3.webp">
</figure>

<figure class="third">
  <img src="/images/beer-pong-table/frame_rails/2.webp">
  <img src="/images/beer-pong-table/frame_rails/4.webp">
  <img src="/images/beer-pong-table/frame_rails/5.webp">
</figure>

<figure class="third">
  <img src="/images/beer-pong-table/frame_rails/6.webp">
  <img src="/images/beer-pong-table/frame_rails/7.webp">
  <img src="/images/beer-pong-table/frame_rails/8.webp">
</figure>


**Assembling the Frame**

<figure class="third">
  <img src="/images/beer-pong-table/frame/0.webp">
  <img src="/images/beer-pong-table/frame/1.webp">
  <img src="/images/beer-pong-table/frame/2.webp">
</figure>

<figure class="third">
  <img src="/images/beer-pong-table/frame/3.webp">
  <img src="/images/beer-pong-table/frame/4.webp">
  <img src="/images/beer-pong-table/frame/5.webp">
</figure>

<figure class="half">
  <img src="/images/beer-pong-table/frame/6.webp">
  <img src="/images/beer-pong-table/frame/7.webp">
</figure>

**Drawing the Outline for the LED Grid on the Upper Lid**

<figure class="half">
  <img src="/images/beer-pong-table/grid/0.webp">
  <img src="/images/beer-pong-table/grid/1.webp">
</figure>

<figure class="half">
  <img src="/images/beer-pong-table/grid/2.webp">
  <img src="/images/beer-pong-table/grid/3.webp">
</figure>

**Countersinking Holes for the LED Grid on the Upper Lid**

<figure class="third">
  <img src="/images/beer-pong-table/grid/4.webp">
  <img src="/images/beer-pong-table/grid/5.webp">
  <img src="/images/beer-pong-table/grid/6.webp">
</figure>

<figure class="third">
  <img src="/images/beer-pong-table/grid/7.webp">
  <img src="/images/beer-pong-table/grid/8.webp">
  <img src="/images/beer-pong-table/grid/9.webp">
</figure>

<figure class="third">
  <img src="/images/beer-pong-table/grid/10.webp">
  <img src="/images/beer-pong-table/grid/11.webp">
  <img src="/images/beer-pong-table/grid/12.webp">
</figure>

<figure class="half">
  <img src="/images/beer-pong-table/grid/13.webp">
  <img src="/images/beer-pong-table/grid/14.webp">
</figure>

**Cutting Support Rails for the Acrylic to Sit Above the Upper Lid**

<figure class="half">
  <img src="/images/beer-pong-table/supports/0.webp">
  <img src="/images/beer-pong-table/supports/1.webp">
</figure>

**Drilling holes for the Connectors on the Ends of the Table**

<figure class="half">
  <img src="/images/beer-pong-table/ends/0.webp">
  <img src="/images/beer-pong-table/ends/1.webp">
</figure>

<figure class="half">
  <img src="/images/beer-pong-table/ends/2.webp">
  <img src="/images/beer-pong-table/ends/3.webp">
</figure>

**Priming the Table with Spray Can Sealer/Primer**

<figure class="half">
  <img src="/images/beer-pong-table/painting/0.webp">
  <img src="/images/beer-pong-table/painting/1.webp">
</figure>

**Laying Out the Electronics**

<figure class="third">
  <img src="/images/beer-pong-table/electronics/0.webp">
  <img src="/images/beer-pong-table/electronics/1.webp">
  <img src="/images/beer-pong-table/electronics/2.webp">
</figure>

**Assembling 20 PCBs for the Cups**

<figure class="third">
  <img src="/images/beer-pong-table/electronics/3.webp">
  <img src="/images/beer-pong-table/electronics/4.webp">
  <img src="/images/beer-pong-table/electronics/6.webp">
</figure>

<figure class="third">
  <img src="/images/beer-pong-table/electronics/5.webp">
  <img src="/images/beer-pong-table/electronics/7.webp">
  <img src="/images/beer-pong-table/electronics/8.webp">
</figure>

**Creating the center LED Grid**

I used enamel coated wire to connect hundreds of LEDs. The wire was wrapped snuggly around the leads to connect the cathodes and anodes of rows and columns. The enamel coating was then melted away during soldering, and proper connections were tested for each lead. This took a LONG time. If I were to do it again I'd definitely figure out a way to use a few LED strips. That way they could be RGB as well.

<figure class="half">
  <img src="/images/beer-pong-table/electronics/9.webp">
  <img src="/images/beer-pong-table/electronics/10.webp">
</figure>

**Securing the Acrylic Support Risers**

![risers](/images/beer-pong-table/assembly/0.webp){:.align-center}

**Adding the Automated Ball Washers**

<figure class="third">
  <img src="/images/beer-pong-table/ball-washer/0.webp">
  <img src="/images/beer-pong-table/ball-washer/1.webp">
  <img src="/images/beer-pong-table/ball-washer/2.webp">
</figure>

**Assembling and Testing all the Electronic Components**

<figure class="half">
  <img src="/images/beer-pong-table/assembly/1.webp">
  <img src="/images/beer-pong-table/assembly/2.webp">
</figure>

{% include video id="ulqUuxT_21k" provider="youtube" %}