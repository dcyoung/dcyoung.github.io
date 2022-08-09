---
title: "Simulating Bin of Objects with Mel in Maya"
date: 2015-04-01T00:00:00-00:00
last_modified_at: 2015-04-01T00:00:00-00:00
categories:
  - game dev
  - 3D
permalink: /post-maya-simulating-debris/
classes: wide
excerpt: Automating/Simulating a bin of objects (teddy bears) using Mel in Maya.
header:
  og_image: /images/maya-simulating-debris/3.jpg
  teaser: /images/maya-simulating-debris/3.jpg
---

![preview](/images/maya-simulating-debris/3.jpg){:.align-center}

In an advanced animation class I worked on an animated short that required a model of a bin of teddy bears. Placing the bears individually seemed like an arduous task, so I wrote a simple script to automate the process. Similar techniques could easily be applied when generating any heap of objects such as piles of trash. The result of simulation is generally more realistic looking than what is achievable by the average hand, or at the very least a good base to work from/tweak

The code here is commented clearly. Reading it should outline the basic process.

```mel
$num = 30; //number of bear duplicates to generate;
//define the reference bear to duplicate
string $ref_bear = "bear0";

//for each bear to be duplicated
for ($i = 1; $i < $num; $i++)
{
	select($ref_bear);
	duplicate - rr;
	select - d;

	//move the bear to a random spot above the bin
	select("bear" + $i);
	$x = rand(-10, 10);
	$y = rand(18, 65);
	$z = rand(-10, 10);
	move $x $y $z;

	//rotate the bear into a random configuration
	$xrot = rand(-90, 90) + "deg";
	$yrot = rand(-90, 90) + "deg";
	$zrot = rand(-90, 90) + "deg";
	rotate - r $xrot $yrot $zrot;
	select - d;

	//make the shape of the bear (just the body part, not the small eyes etc.) a rigid body
	select("bear" + $i + "Shape");
	rigidBody - n - active;
	select - d;
}

//select all the rigid bodies to add a gravity field
$rigidBodies = `ls - type rigidBody`;
select($rigidBodies);
delete ($rigidBodies);
//user still has to add gravity manually after all the rigid bodies are selected

//animate the simualtion. Then go to solvers -> initial state -> set all dynamic

//then select all rigid bodies again, and delete them. This helps with exporting the finished thing
$rigidBodies = `ls - type rigidBody`;
select($rigidBodies);
delete ($rigidBodies);
```

<figure> 
  <img src="/images/maya-simulating-debris/0.jpg">
  <figcaption>Modeling the bin</figcaption>
</figure>
<figure class="half">
  <img src="/images/maya-simulating-debris/1.jpg">
  <img src="/images/maya-simulating-debris/2.jpg">
  <figcaption>Prepping the scene before running the script (left) and after running the script (right).</figcaption>
</figure>

<figure class="half">
  <img src="/images/maya-simulating-debris/3.jpg">
  <img src="/images/maya-simulating-debris/4.jpg">
  <figcaption>Results after running the simulation.</figcaption>
</figure>
