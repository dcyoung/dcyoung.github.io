---
title: "A-Symmetrical Multiplayer Survival FPS"
date: 2014-01-01T00:00:00-00:00
last_modified_at: 2014-01-01T00:00:00-00:00
categories:
  - game dev
  - unreal engine
  - 3D
permalink: /post-a-symmetrical-multiplayer-survival-fps/
classes: wide
toc: true
excerpt: Development and prototyping of a chaotic phsyics driven game.
header:
  og_image: http://img.youtube.com/vi/5BojP7bC5UU/0.jpg
  teaser: http://img.youtube.com/vi/5BojP7bC5UU/0.jpg
---

{% include video id="5BojP7bC5UU" provider="youtube" %}

## Idea

The premise of this game is simple.  You have two options of play.  

- Control a massive monster in a "Pac-Man-esque" top down control scheme.
- Control one of multiple humanoids from a first person perspective in a realistically rendered world.

Both options control characters that exist in the same world space. However while the humanoid players see a realistically rendered world with a terrifying full scale monster, the single monster player sees a grossly simplified top-down arcade style version of the same world space. The objective of the monster is to intersect his arcade sprite with the moving representations of the humanoids.  The monster has a charge up ability that permits it to break through walls. Although from the monster's perspective this activity is simplistic, from the humanoid perspective the events are far more dramatic. The maps are built to be completely destructible so that the monster may physically break through walls in a chaotic and exhilarating manner.

<figure class="half">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/demo_a.png">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/demo_b.jpg">
</figure>

## Objectives

There are few goals of this project...

- Create a comical juxtaposition between the perspectives of playable characters
- Create an entertaining sandbox to experiment w/ unwarranted amounts of Real-Time Physics
  - Real-Time Destructible Environments
  - Physical Collisions
  - Particle Based Fluid Dynamics

## Character Design

### Humanoid

The method by which the humanoids interact with the monster will affect their design. It has yet to be decided what offensive capabilities the humanoids will possess. While the intent of the game is a-symmetry and survival, it would be nice to offer tactics for the humanoid characters to indirectly damage the monster. For example laying traps.

### Monster

An exact design for the monster has not yet been selected, however the two main options being considered are:

- Dinosaur (T-rex) style biped.
- King Kong/gorilla style quadruped. 

Influence is drawn heavily from the following resources I've collected around the web including a specific model by Josh Singh (M-Rex).  I have contacted him for licensing but haven't heard back. 

<figure class="third">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/monster_7.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/monster_2.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/monster_6.jpg">
</figure>
<figure class="third">
<img src="/images/a-symmetrical-multiplayer-survival-fps/monster_1.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/monster_3.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/monster_4.jpg">
</figure>
<figure class="half">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/monster_5.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/monster_0.jpg">
</figure>

## Perspective Design

### First Person Humanoid
<figure class="third">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/fps_0.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/fps_1.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/fps_2.jpg">
</figure>
<figure class="half">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/fps_3.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/fps_4.jpg">
</figure>

### Top Down Arcade

<figure class="third">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/td_3.png">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/td_1.jpg">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/td_2.png">
</figure>
<figure class="third">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/td_0.png">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/td_4.png">
  <img src="/images/a-symmetrical-multiplayer-survival-fps/td_5.jpg">
</figure>


## Prototyping Destructible Assets

The objectives of this game rely heavily on grandiose Hollywood style destruction. The terror of the first person perspective is rooted in dramatic scenes of monsters bursting through walls and debris flying every direction. The humor of the arcade style monster perspective is knowing that the overly simplified sprite animations on screen are actually the same dramatic debris explosions for other characters. Therefore the more realistic and extravagant the destruction, the better.  

When designing destructible environments, I've adopted the following rough pipeline...

- Create 3D model of object using 3dsMax, or other modelling software.
- Create multi-layered fracture patterns for the meshes using RayFire plugin for 3dsMax or Nvidia PhysXLab.
- Import the fractured meshes into UE4 as destructible assets.
- Build environment in UE4 using destructible actor instances of those destructible assets. 
- Code up collision detection and event handling in UE4.
- Program destruction of pre-fractured meshes and chunk behavior in C++ with Nvidia PhysX and APEX SDK.

Some early experimentation with different fracture patterns is shown in the video below. The experimentation includes glass, drywall, concrete, and wood.

## Update 1: Testing Fracture Patterns

This is some of my original experimentation from the first week I downloaded ue4. I believe the project was made on engine version 4.2, but later imported into 4.4 to make these videos. Some of the depth levels and destructible mesh settings were corrupted in the import, but it still gives the right idea.

{% include video id="rZrofOEnDco" provider="youtube" %}

## Testing Animated Actor Collisions

Again, this is some of my original experimentation with ue4. I believe the project was made on engine version 4.2, but later imported into 4.4 to make these videos. Some of the depth levels and destructible mesh settings were corrupted in the import, but it still gives the right idea. I wanted to see if an animated mesh (in this case a moving sphere controlled by a button) could collide with DMs and trigger destruction.

{% include video id="K-89ZxjdbUs" provider="youtube" %}

## Animated T-REX Actor Collision

Again, this is some of my original experimentation with ue4. I believe the project was made on engine version 4.2, but later imported into 4.4 to make these videos. Some of the depth levels and destructible mesh settings were badly corrupted in the import for this version in particular because the wood in the walls splintered all wrong (looks more like straight cuts than splinters).

​The model was pulled from an old Turok game. This is simply personal experimentation, no distribution whatsoever.

{% include video id="5BojP7bC5UU" provider="youtube" %}

{% include video id="0khkQrKQJuc" provider="youtube" %}

## Experiment with C++ PhysX

I did a bit of experimenting with C++ to see how I could manipulate chunks directly. I've covered this in more detail in a separate post. This may yield some very fun gameplay features in the future, but mostly I was hoping to gain insight on how to force certain chunk behaviors when the physics simulation won't produce the desired look or feel (ie: hollywood-ize the destruction). I remade the demo in v 4.9 recently to record the video below. It only applies forces to chunks that aren't sleeping, so if a chunk stops moving for long enough it falls asleep and won't have force applied. This behavior is completely modifiable but will be very useful in keeping the number of awake bodies down which should benefit performance.

{% include video id="3uIC5kSBoQs" provider="youtube" %}

## Playable T-rex Character Test

Eventually the game design will call for a monster AI (for single player experience) or a comical 2d perspective for the player controlling the monster (for a multiplayer player experience). For now though, the AI is still under heavy planning and the 2d stuff will come later. I wanted to see what the Trex would look like moving around, so I decided to make a character to check out the various animations in different blendspaces.

{% include video id="MTkfPVtjlss" provider="youtube" %}

Currently the character is setup with a movement component and in place animations blended together based on user inputs and character velocity. Unfortunately this lends itself to a common problem called skating, where a character's movement doesn't completely match the animation and the character appears to skate along the ground. This is a typical problem resulting from the use of in-place animations glued to a movement component. In such setups, a bounding box or capsule determines the movement, speed, and direction while the player model and animations are just along for the ride like a puppet on a moving stage. However, the ease of implementing this solution means it monopolize core strategies for animation and movement. Very intricate blend spaces and simple tricks to increase visual fidelity of this "puppet show", are usually better alternatives than adopting a different core strategy.

BUT.... this isn't my goal for the end game. Instead of having a movement component and updating the animation based off a blend space (like shown in the demo above), I intend to base movement off root motion of the animations instead. This will be highly unorthodox, contrary to every normal method of creating a movable character. I'm pursuing root motion because I intend to have the Trex on a grid, where movement is only permitted forward, backward or in complete turns... think pacman. All turning animations will be complete 90 or 180 degree rotations.

## Destructible Mesh Framing

I've been experimenting with world support settings and how I can get different assets to seem like they are connected to a frame underneath. This will be useful for walls with frames and concrete with Rebar. The assets below haven't been setup correctly yet for reasonable collision with anything, so they kind of explode... but it shows the idea of frames. Eventually I'll build the frames themselves out of destructible meshes and swap out complex meshes like the rebar for altered versions that look bent upon collision.

{% include video id="eBx7gEYxtR4" provider="youtube" %}

## Destructible Floor

This was a quick prototype that yielded pretty fun results. I added some custom animation notifications at the same key frames as the footstep sound animation notifies. The custom notifications would run a bit of code to determine the location of the foot bone and apply a radial force with a drop-off at that location. The result is a big impact directly under the foot and spider-cracks out from it. The wood assets were made hastily in PhysXLab and could use a lot more attention. But the basic assets should still convey how simple and effective the concept is.

{% include video id="DzQKhmVQkBM" provider="youtube" %}