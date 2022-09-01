---
title: "Visualizing Runtime Flowpath in VR"
date: 2016-05-01T00:00:00-00:00
last_modified_at: 2016-05-01T00:00:00-00:00
categories:
  - game dev
  - virtual reality
  - 3D
permalink: /post-visualizing-runtime-flowpath-in-vr/
classes: wide
toc: true
excerpt: An interactive Virtual Reality sandbox for the creation of digital logic circuits and graphical scripting
header:
  og_image: http://img.youtube.com/vi/s0wEFLmifPM/0.jpg
  teaser: http://img.youtube.com/vi/s0wEFLmifPM/0.jpg
---

{% include video id="2rHeg_TymeE" provider="youtube" %}

The following is a development blog of sorts documenting a Virtual Reality and Leap Motion project built for a VR course at UIUC. The experience is an interactive Virtual Reality sandbox for the creation of digital logic circuits and graphical scripting. The goal was to visualize runtime flowpath in the context of interactive circuits formed of finite primitive elements.

## Project Proposal

{% include pdf-embed.html url="/images/runtime-flowpath-vr/proposal.pdf" %}

## Representing and Solving Digital Logic Circuits

**(March 23rd, 2016)**

The final project will most likely be built in Unity, which uses C#. I was away from home today with only my laptop so I drafted up some code in C# separate from the Unity engine. The idea was to construct a back-end representation for the circuit elements and their connection. A directed graph is a logical choice. To solve the directed graph I implemented a simple topological sort.

The code for this can be viewed here: ​[github.com/dcyoung/CircuitSolver](https://github.com/dcyoung/CircuitSolver)

The implementation of the directed graph uses adjacency lists (stored in a dictionary map) to describe edges. This is a directed graph, so only one-way mapping is required to describe the edges... but maps for both parental and child relationships are maintained to ease some other operations elsewhere in the code base. The only adjacency list necessary for the topological sort is the dependents (children).

```csharp
private List<Node> nodes;
private Dictionary<Node, List<Node>> dependencies;// mapping edges for dependencies
private Dictionary<Node, List<Node>> dependents;  // mapping edges for dependents
```

Then, the topological sort is performed using a recursive depth first search. The visited node markers are held in a map and the final sorted order is held in a stack.

```csharp
private Stack<Node> reversePost;
private Dictionary<Node, bool> marked;
// ...
/**
 * Sorts the circuit's nodes in topological order such that all dependencies of nodes preceed the node
 */
public Stack<Node> topologicalSort()
{
	//create a new stack to hold the final order
	reversePost = new Stack<Node>();
	//reset all the marked flags to false
	marked = new Dictionary<Node,bool> ();
	foreach(Node n in this.nodes)
	{
		marked.Add (n, false);
	}
		
	//Perform a Depth First Search (DFS) to topologically sort the directed graph
	foreach( Node n in this.nodes )
	{
		if(!marked[n])
		{
			depthFirstSearch (n);
		}
	}

	return reversePost;
}
	
/**
 * Recursive Helper Function for the topological sort
 */ 
private void depthFirstSearch(Node n)
{
	marked [n] = true;
	foreach(Node child in this.getChildrenOfNode(n))
	{
		if( !marked[child] )
		{
			depthFirstSearch (child);
		}
	}
	reversePost.Push (n);
}
```

This topological sort can be used to solve the circuit as follows.

```csharp
/**
 * Solves the digital logic circuit by performing a topological sort
 * on all the nodes, before determining the active state of each in 
 * that order based off their inputs (active states of their parents).
 */ 
public void solve()
{
	//topologically sort the nodes so that every node comes after any dependencies
	Stack<Node> sortedNodes = this.topologicalSort ();

	//for each node, set the active state by processing the inputs to the node (inputs are 
	//just the activeState of the dependencies (parent nodes)... which in turn were determined
	//previously by the activeState of their parents and so on... all the way to the top where the
	//source processInputs() fxn simply returns the current activeState of the source node.
	Node next;
	while( sortedNodes.Count > 0 )
	{
		next = sortedNodes.Pop ();
		next.setActiveState (next.processInputs (this));
	}
}
```

## Getting Up and Running in Unity 

**(March 31st, 2016)**

I threw together a git repo for the project and migrated the RAW C# code into a unity project.

The project can be obtained here: [github.com/dcyoung/FlowPath.git](https://github.com/dcyoung/FlowPath.git)

​Right now it just performs the basic circuit test when the game starts and prints out info to the console. So the backend is working in Unity.


## Leap Motion For Moving Primitive Objects 

**(April 7th, 2016)**

The new Orion SDK for the leap motion controller is miles ahead of the older SDK, but modules and example content have been slow to release. As of now, the only supported gesture is a "pinch" motion with the thumb and pointer finger. While some wonderful demos, specifically the cube demo, demonstrate the pinch motion working to great effect... I have yet to find source code or example projects for object interaction. I spent an hour or two tonight tinkering with the pinch motion demo scene and managed to whip up a quick & dirty SPIKE solution for interacting with objects. I'm still new to unity, with all my background in UE4, so most of my time was spent figuring out how to deal with unity's interface.

The simple code: [github.com/dcyoung/FlowPath/blob/master/FlowPath/Assets/InteractiveObjects/Scripts/ItemPickup.cs](https://github.com/dcyoung/FlowPath/blob/master/FlowPath/Assets/InteractiveObjects/Scripts/ItemPickup.cs)

{% include video id="kmGyBRXWIaE" provider="youtube" %}

## Leap Motion Continued

**(April 12th, 2016)**
I spent some more time messing around with the project trying to get a trigger volumes to serve as parts bins. There seems to be some
unpredictable behavior when querying the "isPinching" variable of a LeapPinchDetector... but I managed to get a primitive instantiated on the exit of the trigger volume instead. I'm sure a better implementation would be easy if I rummaged through the PinchDetector source... but this works for now. Again, the thumb seems to be the ideal positional locator for this stuff. 

I wrote a class to handle the interaction that spawns an interact-able primitive... and because it shared enough code with the ItemPickup class from the previous update, I extracted the common elements into an ItemInteraction class that both subclasses can inherit from. 

See the source: [github.com/dcyoung/FlowPath/tree/master/FlowPath/Assets/InteractiveObjects/Scripts](https://github.com/dcyoung/FlowPath/tree/master/FlowPath/Assets/InteractiveObjects/Scripts)

{% include video id="f4uIxsnu8Y4" provider="youtube" %}

## Tested VR Support + Event Based Interaction Locks

**(April 20th, 2016)**

​I finally got the leap motion and a DK2 in one place at the same time and managed to give the project a go in VR. All I can say is WOW... it works a lot better with a headset. If leap motion ever seemed at all "gimicky", then try it with a VR headset and see for yourself. Its surreal. Also the "Cubes" demo from the developer gallery on the Leap Motion site is brilliant in VR. I thought it was rather good when I just had the leap motion strapped to a hat, but it was an entirely different experience with the DK2. I can't wait for my CV1 to get here so I can give it a whirl with oculus runtime v1.3.

After playing around with the project in VR for a bit, I got sick of multiple primitives attaching to the hand simultaneously. I experimented with an "event" based notification system that alerts subscribers of newly engaged interactions and newly terminated interactions. This lets each interactive item shut itself off to the possibility of interaction until it is notified that all other interactions have concluded... ensuring 1 interaction is active at a time. 

## Part Bin Model 

**(April 23rd, 2016)**

I figured I'd spruce up the aesthetic while prototyping the mechanics. I whipped up a model in Maya for an extremely simple parts bin. The model is nothing to write home about, but it adds a little more context to the scene compared to blank trigger volumes.

![bin](/images/runtime-flowpath-vr/bin.jpg)

## Interaction Mode Selection

**(May 5th, 2016)**

With large collision boxes and multiple types of interactions I decided to split up the interactions into categories that only work in certain modes. This will work like tools in a modeling program for example, where you must select the right mode before using a tool relevant to that category. At minimum there need to be at least 3 dedicated modes for the following:

- Creating/moving primitives
- Creating/editing connections
- Spectating

I reworked the classes a bit to make them more universal and ended up with the following: There is now a dedicated static event manager for switching modes. Mode support can be cycled.. allowing for many different kinds of modes. Alert delegates/events are sent out upon change in mode and receivers can handle things accordingly. For example I created a textUpdate component script that updates the text on the button face plate when the events fire. Similarly, a check is made in the item interaction script to ensure that the "Move" mode is enabled before letting the user spawn or move primitives. This new system is universal and easily expanded. I tested it all with leapmotion and its working.

{% include video id="s0wEFLmifPM" provider="youtube" %}

## Connection Mode Early WIP 

**(May 8th, 2016)**

Few updates here:

- Refactored a bit of the mode selection.
- Added dynamic instructions/message display that subscribes to the various event managers. This way I can present appropriate instructions for the user based off the game state as well as provide step-by-step instructions that only progress when the user completes the steps.
- Added a circuit manager to interface with the backend.
- Various bug fixes.
- Progress made on interactive specification of connection ports + translating front end interaction to backend updates.

{% include video id="KxBMjklltd8" provider="youtube" %}

## Successful Integration of Front + Backend

**(May 9th, 2016)**

Bunch of updates here:

- Various bug fixes in the backend circuit code. Previously the code did not permit nodes to have missing parents and would error when solving a circuit. I implemented a more robust check that will also set active states properly in situations without a parent node (ex: an OR gate with only 1 active parent now appears active).
- Circuit is now solved whenever an element on the front end changes in a way that might change the circuit.
- Front end node representations now have a visual cue indicating if they're active. The cue is updated using the CircuitManager event system whenever the circuit is updated... this keeps the front and back end in sync.
- Added source gates to the scene and implemented a control switch to change the source value (on or off) in real time which propagates changes through the rest of the circuit.

{% include video id="NSHfKCdbMU0" provider="youtube" %}


## Visualizing Connections 

**(May 11th, 2016)**

Lots of updates in this iteration.
- Various bug fixes
- New meshes for ports. A fellow classmate created these new models for a port, and they worked out fine.

![ports](/images/runtime-flowpath-vr/connections.jpg){:.align-center}

- Enhanced visual cues for specifying a prospective connection. With a latent prospective connection, only the output ports are shown for selection. Once one has been selected, it is highlighted green for reference but is not interactive. All the other output ports are visually removed so the user select a valid input port. Once an input port is selected the connection is automatically completed and the user can begin specifying another connection. This keeps things very snappy for fast circuit builds. I experiemnted with a setup where the user specifies a prospective connection and then hits a button to submit it, but it seemed too cumbersome. Once you're used to the leap motion system you can really quickly prototype circuits. ​

<figure class="half">
    <img src="/images/runtime-flowpath-vr/interaction_1.jpg">
    <img src="/images/runtime-flowpath-vr/interaction_2.jpg">
</figure>

- Procedural Mesh generation for connections
  - Uses a custom tube renderer to render a tube around a physics driven rope. The physics look great, but can spazz out in certain conditions. Right now the physics are effectively disabled. Some hacky workarounds could keep them under control, but I have a good fix in mind thats in the works.
- New meshes for primitives (again a classmate created these). 
- Simple holographic rotating icon above each node. This helps display the node type while keeping the node a more simple and compact mesh. The custom new meshes for primitives mentioned above were used for the hologram.

![hologram](/images/runtime-flowpath-vr/hologram.jpg){:.align-center}

Here is a short video showing a simple circuit. There are still a few update bugs that need to get fleshed out and also I forgot to demonstrate the updated tubes when connected nodes are moved. I'll get another video out soon showing all this.

{% include video id="2rHeg_TymeE" provider="youtube" %}

## Minor Documentation Improvements

**(May 12th, 2016)**

The code is fairly well documented or self explanatory, save for missing summaries at the top of classes. I intend to do a full sweep of everything and refactor/document. In the meantime I threw some brief summaries on the ReadMe for the git repo.
You can see the WIP notes here: [github.com/dcyoung/FlowPath](https://github.com/dcyoung/FlowPath)