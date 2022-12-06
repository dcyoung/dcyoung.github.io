---
title: "Hybrid Control of a Self Balancing Robot"
date: 2015-12-01T00:00:00-00:00
last_modified_at: 2015-12-01T00:00:00-00:00
categories:
  - robotics
permalink: /post-self-balancing-robot/
classes: wide
toc: true
excerpt: Designing a hybrid controller for a self-balancing robotic pendulum.
header:
  og_image: /images/self-balancing-robot/preview.webp
  teaser: /images/self-balancing-robot/preview.webp
---

{% include video id="kjRBskEKIeU" provider="youtube" %}

## Introduction to the Pendubot, Retrieving and Filtering Signals

{% include pdf-embed.html url="/images/self-balancing-robot/1-intro-filter.pdf" %}

## Oscillating Movement

{% include pdf-embed.html url="/images/self-balancing-robot/2-oscillating-movement-simple.pdf" %}

## PID Controllers

{% include pdf-embed.html url="/images/self-balancing-robot/3-oscillating-movement-pid.pdf" %}

## Robot Animator

{% include pdf-embed.html url="/images/self-balancing-robot/4-transformations-and-animations.pdf" %}

## Simulating Movement with Lagrangian Dynamics

{% include pdf-embed.html url="/images/self-balancing-robot/5-lagrangian-dynamics-theoretical-parameters.pdf" %}

## Enhancing Simulation with the Hamiltonian

{% include pdf-embed.html url="/images/self-balancing-robot/6-hamiltonian-experimental-parameters.pdf" %}

## Designing a Hybrid Controller

{% include pdf-embed.html url="/images/self-balancing-robot/7-hybrid-controller-extra.pdf" %}

## Controlling the Robot with a Kinect Sensor

{% include video id="75_WzvI9v3o" provider="youtube" %}

I wanted to take the Pendubot a step further and the robotics lab on campus happened to have a few extra Microsoft Kinects laying around. What better fun that controlling a robot by waving your hands! There were a few design considerations that had to be fleshed out however.

- The robot hardware was all setup with a computer running Matlab r2012b which makes implementing data acquisition for the kinect sensor a much more tedious process involving 3rd party solutions. Matlab r2013+ introduced much more simple implementations.
- I had access to a computer running Matlab r2013b, but conducting the data acquisition on a different PC meant communicating that information over a network.
- Assuming the network connection was operational in Matlab, there were still two functions that needed to execute simultaneously... 1) Simulink model controlling the robot... and 2) the client script receiving updated info from the server. Also the robot controller would still have to run lightning fast, whereas the updated commands from the server could come in relatively slowly (~20/second). Without being able to put the call in the control loop itself, the solution solution would have to involve two asynchronously parallel function. Of course Matlab doesn't lend itself to simple asynchronous parallelism. Although there are some workarounds -- I later discovered this was unnecessary, as the model was running externally and a simpler solution would suffice.

### Drafting a Client + Server to Acquire + Retrieve Kinect Data

```matlab
%%%%%%%%%%%%%%%    CLIENT     %%%%%%%%%%%
clear all; close all; clc;
tcpipClient = tcpip('172.16.1.71',55000,'NetworkRole','Client') %for
% server running on kinect computer

set(tcpipClient,'InputBufferSize',8);
set(tcpipClient,'Timeout',1000);
fopen(tcpipClient);
while(1)
    rawData = fread(tcpipClient,1,'double');
    display(rawData);
    if rawData == 0
        set_param('Hybrid_Controller/c','Value','0');
    elseif rawData == 1
        set_param('Hybrid_Controller/c','Value','1.57');
    else
        set_param('Hybrid_Controller/c','Value','-1.57');
    end
end
fclose(tcpipClient);
display('successfully retrieved data from server');
```

```matlab
%%%%%%%%      Rough SERVER Draft    %%%%%%%%%%%%
close all; clear all; clc;

%define data to send over network as a 1x1 array (for simple command code)
dataPackage = zeros(1,1);
s = whos('dataPackage')

%define server and open it
tcpipServer = tcpip('0.0.0.0',55000,'NetworkRole','Server');
set(tcpipServer,'OutputBufferSize',s.bytes);
display('Initialized Server');
fopen(tcpipServer);
display('Acquired Client, beginning Kinect Setup');

%setup path for kinect stuff
utilpath = fullfile(matlabroot, 'toolbox', 'imaq', 'imaqdemos', ...
    'html', 'KinectForWindows');
addpath(utilpath);

% The Kinect for Windows Sensor shows up as two separate devices in IMAQHWINFO.
hwInfo = imaqhwinfo('kinect');

% Create the VIDEOINPUT objects for the depth streeam, which is the 2nd device
depthVidOBJ = videoinput('kinect',2);

depthVidOBJ.TriggerRepeat = Inf;
depthVidOBJ.FrameGrabInterval = 1;

% Get the VIDEOSOURCE object from the depth device's VIDEOINPUT object.
depthSrc = getselectedsource(depthVidOBJ);

% Turn on skeletal tracking.
depthSrc.TrackingMode = 'Skeleton';

%turn on the stream
start(depthVidOBJ)

%we will always be dealing with the first frame since we deal with them one at a time here
frameInQuestion=1;

acquireCount = 50; %determines how long the data acquisition will continue for
fprintf('Initiating Data Acquisition\n\n');
while(1)%acquireCount >=0)
        %acquire the data
        [frameDataDepth, timeDataDepth, metaDataDepth] = getdata(depthVidOBJ);

        anySkeletonsTracked = any(metaDataDepth(frameInQuestion).IsSkeletonTracked ~= 0);
        if(anySkeletonsTracked)            
            % See which skeletons were tracked.
            trackedSkeletons = find(metaDataDepth(frameInQuestion).IsSkeletonTracked);
            
            % Skeleton's joint indices with respect to the color image
            jointIndices = metaDataDepth(frameInQuestion).JointImageIndices(:, :, trackedSkeletons);

            %define specific joint Indices
            rightHand= jointIndices(8,:);
            leftHand= jointIndices(12,:);


            %check for control gestures (currently simple 2 hand control gestures)
            if(abs(rightHand(2)-leftHand(2))>25) %are the hands around the same heigh
                if(rightHand(2)>leftHand(2))
                    fwrite(tcpipServer,dataPackage(:),'double');
                    display('Move Robot Right');
                    dataPackage(1)=2;
                else
                    display('Move Robot Left');
                    dataPackage(1)=1;
                end
            else
                display('Keep Robot In Place');
                dataPackage(1)=0;
            end
            fwrite(tcpipServer,dataPackage(:),'double');
        else
            display('No skeleton detected');
        end
    acquireCount = acquireCount-1;
end

stop(depthVidOBJ)
fprintf('\nDone Acquiring Data\n');


fclose(tcpipServer);
display('Successfully closed server');
```

### Designing an Asynchronous Parallel Client

After spending a great deal of time experimenting with asynchronous parallelism in Matlab (including getting into some java threading behind the scenes) it dawned on me that the controller was actually being run externally. I felt quite silly for wasting so much time but it was good experimentation nonetheless. In the end providing instructions to the model transformed into a dramatically simple task. To take care of the updates I used a "parameter set" command in the client that targeted a variable in the model and executed on update from the server.
