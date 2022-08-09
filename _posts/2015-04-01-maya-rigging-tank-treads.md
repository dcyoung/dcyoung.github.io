---
title: "Rigging Tank Treads with Mel in Maya"
date: 2015-04-01T00:00:00-00:00
last_modified_at: 2015-04-01T00:00:00-00:00
categories:
  - game dev
  - 3D
permalink: /post-maya-rigging-tank-treads/
classes: wide
excerpt: Programmatic rigging of tank treads in Maya.
header:
  og_image: /images/maya-rigging-tank-treads/4.jpg
  teaser: /images/maya-rigging-tank-treads/4.jpg
---

## Version 2.0

Version 1.0 was a good exercise to get acquainted with MEL, but the project had a few bugs. So I rebuilt it from the ground up with a much more robust rig. The apparent flipping is no longer an issue and the rig is completely scale-able and controllable. The final rig allows tracks to move realistically regardless of the orientation of the model and also has fine tuning per track to account for unpredictable situations. The result was very useful in quickly animating the movement of a robot with treads in a short for my advanced animation class.

<figure class="half">
  <img src="/images/maya-rigging-tank-treads/0.jpg">
  <img src="/images/maya-rigging-tank-treads/2.jpg">
</figure>

<figure class="half">
  <img src="/images/maya-rigging-tank-treads/1.jpg">
  <img src="/images/maya-rigging-tank-treads/3.jpg">
</figure>

## Version 1.0

To get acquainted with the scripting language of maya called MEL (Maya Embedded Language) I decided to tackle a small expression for a tank tread/track assembly. The idea was to have a track moveable with a single rig handle that will animate automatically when translated. It uses some extremely basic geometry to calculate the location of each tread along a curve that defines their paths. Some extra functionality like rigged clusters keep the track a little more interesting, but if I were to do it again I would add some more clusters as well as a dynamic weighted path to add effects of inertia and rebound.

![v1](/images/maya-rigging-tank-treads/4.jpg){:.align-center}

```mel
int $numTreads = 36;
string $pathNames[];
for ($i = 1; $i < ($numTreads + 1); ++$i)
{
	$pathNames[$i - 1] = "motionPath" + $i;
}

float $Zdist = TrackLeft_Control.translateZ;
float $circumference = curveInfo1.arcLength;
int $direction;

//this is actually the forward direction
if ($Zdist < 0)
{
	$direction = -1;
	reverseCurve1.nodeState = 1;

	//motionPath1.inverseFront = 1;
	for ($pathName in $pathNames)
	{
		setAttr($pathName + ".inverseFront") 1;
	}
}
else
{
	$direction = 1;
	reverseCurve1.nodeState = 0;

	//motionPath1.inverseFront = 0;
	for ($pathName in $pathNames)
	{
		setAttr($pathName + ".inverseFront") 0;
	}
}

/* Determine the uValue of the first tread... that will serve as a reference for the rest */
float $uValue = $direction * ($Zdist % $circumference) / $circumference;

/* Set the uValues for each tread */

float $treadOffset = 1.0 / $numTreads; //can't forget the 1.0 to convert to float
float $uValueSpecific;				   //this will hold the specific offset uValue for each tread

for ($i = 0; $i < $numTreads; ++$i)
{

	$pathName = $pathNames[$i];

	$uValueSpecific = ($uValue + ($i * $treadOffset)) % 1;

	setAttr($pathName + ".uValue") $uValueSpecific;

	/*Account for the weird inversion of treads in certain parts of the track... found by trial and error. 
		The source of this inversion is still unclear... but this is a ghetto fix.*/
	if ($Zdist <= 0)
	{
		if ($uValueSpecific > 0.6205 && $uValueSpecific < 0.8745)
		{
			setAttr($pathName + ".inverseUp") 0;
		}
		else
		{
			setAttr($pathName + ".inverseUp") 1;
		}
	}
	else
	{
		if (($uValueSpecific < 0.685 && $uValueSpecific > 0.105) || ($uValueSpecific < 1 && $uValueSpecific > 0.91) || ($uValueSpecific < 0.001))
		{
			setAttr($pathName + ".inverseUp") 1;
		}
		else
		{
			setAttr($pathName + ".inverseUp") 0;
		}
	}
}

/* Rotate the inner Wheels */
big_wheel.rotateY = -360 * $Zdist / (3.14159 * 20.078);
pasted__big_wheel.rotateY = -360 * $Zdist / (3.14159 * 9.322);
pasted__pasted__big_wheel.rotateY = -360 * $Zdist / (3.14159 * 10.321);
```
