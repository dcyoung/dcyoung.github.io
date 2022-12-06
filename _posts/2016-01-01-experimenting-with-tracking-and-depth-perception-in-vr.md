---
title: "Experimenting with Tracking & Depth Perception in VR"
date: 2016-01-01T00:00:00-00:00
last_modified_at: 2016-01-01T00:00:00-00:00
categories:
  - game dev
  - virtual reality
  - 3D
permalink: /post-experimenting-with-tracking-and-depth-perception-in-vr/
classes: wide
excerpt: Minor experiments in VR.
header:
  og_image: /images/virtual-reality-depth-perception/preview.webp
  teaser: /images/virtual-reality-depth-perception/preview.webp
---

​This experiment was meant to highlight the difference between rotation and position tracking as an element of VR experiences, as well as investigate how depth perception relies on both forms of tracking. The written code includes scripts to mirror a user's head movement (position and orientation), disable positional tracking, disable rotational tracking and reposition stimuli of various sizes to appear as similar sizes at the same depth. Although these tasks may seem trivial, the process of disabling rotational tracking in Unity using OVR can be tricky. Hopefully the included code helps a few people out there struggling to find a solution given the limitations of the OVR assets.

## VR Mirror

This simple script creates a Virtual Reality Mirror of sorts. It considers the tracked position and orientation of the head mounted display and then manipulates a game object's rotation and position to match or mirror the pose. The difference between mirroring and matching is whether the object is facing the camera. If the object is matching movements, then if you bring your face closer to the screen, the object moves further away from the screen. If the object is mirroring movements, then bringing your face closer to the screen will move the object closer to the screen as well.

```csharp
using UnityEngine;
using System.Collections;

public class VRMirror : MonoBehaviour
{
    public CameraFlipper cameraFlipper;
    public GameObject copyCat;
    private Vector3 copyCatStartingPosition;
    private Transform eyeCenter;

    // Use this for initialization
    void Start()
    {
        eyeCenter = transform.Find("TrackingSpace/CenterEyeAnchor");
        copyCatStartingPosition = copyCat.transform.position;
    }

    // Update is called once per frame
    void Update()
    {

        if (cameraFlipper.getShouldMirror())
        {
            /**
            * Make the cube mirror your movements (positional and
            * rotational). This means that the cube is facing the camera (and as a result, the user should
            * see the cube’s face). In this case, if you bring your face close to the screen, the cube moves
            * closer to the screen as well. Imagine looking into a mirror to get an intuition of this.
            */
            //NOTE: 
            //This implementation has the copy cat mirror the player's movement but does this mirroring in its own frame (relative to its starting position)
            //The offset of the player's movement is equal to the position of the eyeCenter relative to the OVRCameraRig
            //Similarly, the copycat logs its starting position for reference later, as its relative origin for mirrored movement. 
            //Doing things this way enables versaitility later, in case one wishes to have many copycat objects in different locations, mirroring the same target.
            OVRPose mirroredPose = eyeCenter.ToOVRPose();
            mirroredPose.orientation *= Quaternion.Euler(0.0f, 180.0f, 0.0f);
            mirroredPose.orientation.w *= -1.0f;
            mirroredPose.orientation.z *= -1.0f;

            mirroredPose.position.z *= -1;
            mirroredPose.position += copyCatStartingPosition;
            copyCat.transform.FromOVRPose(mirroredPose);
        }
        else
        {
            /**
            * Make the cube match your movements. This includes
            * positional and rotational movements . Furthermore, note that this also means that the cube
            * should be looking in the same direction the camera is (and as result, the user should see the
            * back of the cube’s head). For example, if you bring your face closer to the screen, the cube
            * moves further away from the screen.
            */
            OVRPose newPose = eyeCenter.ToOVRPose();
            newPose.position = newPose.position + copyCatStartingPosition;
            copyCat.transform.FromOVRPose(newPose);
        }
    }
}
```

---

## Disabling Position and Rotation Tracking

The following script provides a means of disabling or rather toggling the position and or rotation tracking of the head mounted display. Being able to selectively toggle the two forms of tracking helps demonstrate how much they contribute to the VR experience.

Although disabling tracking is generally a bad idea, there do exist reasons for a developer to want the build in tracking disabled. Perhaps a developer wants to implement their own form of tracking, or simply prefers to have the executive choice to do so. Ideally the development tools available would have simple toggles for these forms of tracking that would cut the tracking process off at the base to save performance. Unfortunately no such toggle exists for rotational tracking when using the OVR assets for the Unity Game Engine. I had to get a little creative with the solution. What I wound up with was a glorified "hack" that counteracted/cancelled the rotation after it was applied. If anyone has a better solution let me know!

Direct transformations cannot be applied the center eye anchors within the tracking space. I'm not sure why, but I assume it has to do with late updates or order of execution internally. Instead the solution involved rotating the parent space (tracking space) such that the updated rotation was effectively cancelled.​

```csharp
using UnityEngine;
using System.Collections;

public class ToggleTracking : MonoBehaviour
{
    private Transform eyeCenter;
    private Transform trackingSpace;
    private bool bUseRotationalTracking = true;
    private bool bUsePositionalTracking = true;

    private Vector3 lastKnownHMDPosition;

    private Quaternion lockedHMD_GlobalOrientation; //used for checking accuracy
    private Quaternion lastKnownHMD_GlobalOrientation;

    void Start()
    {
        eyeCenter = transform.Find("TrackingSpace/CenterEyeAnchor");
        trackingSpace = transform.Find("TrackingSpace");
    }

    // Update is called once per frame
    void Update()
    {
        checkForInput();
    }

    void LateUpdate()
    {
        if (!bUsePositionalTracking)
        {
            counteractTranslation();
        }
        if (!bUseRotationalTracking)
        {
            counteractRotation();
        }
    }

    void checkForInput()
    {
        //Pressing the R key should toggle rotation tracking on and off.
        if (Input.GetKeyDown("r"))
        {
            bUseRotationalTracking = !bUseRotationalTracking;
            print("Toggling rotation tracking to " + bUseRotationalTracking);
            if (!bUseRotationalTracking)
            {
                lastKnownHMD_GlobalOrientation = eyeCenter.transform.rotation;
                lockedHMD_GlobalOrientation = eyeCenter.transform.rotation;
            }
        }

        //Pressing the P key should toggle position tracking on and off.
        if (Input.GetKeyDown("p"))
        {
            bUsePositionalTracking = !bUsePositionalTracking;
            print("Toggling positional tracking to " + bUsePositionalTracking);
            if (!bUsePositionalTracking)
            {
                lastKnownHMDPosition = eyeCenter.transform.position; // ToOVRPose().position;
            }
        }
    }

    //counteracts any positional changes 
    void counteractTranslation()
    {
        Vector3 currentHMDPosition = eyeCenter.transform.position;
        Vector3 deltaPosition = currentHMDPosition - lastKnownHMDPosition;
        trackingSpace.position -= deltaPosition;
    }

    //counteracts any additional tracked rotation of the headset by rotating its parent tracking space to negate the tracked rotation
    void counteractRotation()
    {
        Quaternion HMD_deltaRotation = lastKnownHMD_GlobalOrientation * Quaternion.Inverse(eyeCenter.transform.rotation);
        trackingSpace.rotation = HMD_deltaRotation * trackingSpace.rotation;
        lastKnownHMD_GlobalOrientation = eyeCenter.rotation;

        //checkAccuracy();
    }

    //Checks the accuracy of the counteracted rotation... 
    //Cmpares the current global orientation of the Center Eye Anchor to the global orientation at the time of disabling tracking
    void checkAccuracy()
    {
        Vector3 diff = lockedHMD_GlobalOrientation.eulerAngles - eyeCenter.rotation.eulerAngles;
        float thresh = 0.01f;
        if (Mathf.Abs(diff.x) > thresh || Mathf.Abs(diff.y) > thresh || Mathf.Abs(diff.z) > thresh)
        {
            print("" + diff.x + ", " + diff.y + ", " + diff.z);
        }
    }
}
```

---

## Depth Perception and Relative Size

This script rearranges game objects so that they appear to be of equal size when viewed. Additionally a small sequence demonstrates the effect by randomly assigning an order to the objects and displaying them one by one. 

```csharp
using UnityEngine;
using System.Collections;

public class GenerateStimuli : MonoBehaviour
{
    public GameObject[] stimulusObjs; //specify the objects in the inspector for use in the stimulus loop
    public GameObject targetEye; //the reference point that will be used to determine how stimuli should be rearranged 
    private bool bSeqInProgress = false; //true for the duration of the displayed stimulus sequence

    public float desiredAngularDiameterInDeg; //will determine the apparent size of all the stimuli
    public float spacingAngleDegrees; //will determine the apparent spacing of the stimuli

    // Update is called once per frame
    void Update()
    {
        checkForInput();
    }

    void checkForInput()
    {
        //Pressing the S key should activate the main sequence, only if any previously activated sequences are finished
        if (Input.GetKeyDown("s"))
        {
            print("received request to run main sequence");
            if (!bSeqInProgress)
            {
                //run the main sequence
                mainSequence();
            }
            else
            {
                print("Main sequence already running");
            }
        }
    }

    //The main sequence I'll be using as an example
    void mainSequence()
    {
        print("initiating main sequence");
        bSeqInProgress = true;
        setAllStimuliActive(stimulusObjs, false);
        randomizeStimOrder(stimulusObjs);
        Vector3[] positionAssignments = determinePositions(stimulusObjs, targetEye, desiredAngularDiameterInDeg, spacingAngleDegrees);
        assignPositions(stimulusObjs, positionAssignments);
        StartCoroutine(showStimuli(stimulusObjs));

    }

    //Activates all stimulus in a target array
    void setAllStimuliActive(GameObject[] objs, bool bStimActive)
    {
        foreach (GameObject stimulusObj in objs)
        {
            stimulusObj.SetActive(bStimActive);
        }
    }

    //Randomize the order of stimuli in an array of stimulus objects
    void randomizeStimOrder(GameObject[] objs)
    {
        ShuffleArray(objs);
    }

    //converts an angle from degrees to radians
    float degToRad(float deg)
    {
        return deg * Mathf.PI / 180.0f;
    }

    //returns the distance an object with "actualDiameter" must be from the view point to yield the desired angular diameter
    float distFromAngDiam(float angularDiameter, float actualDiameter, bool bAngDiamProvidedInRadians)
    {
        float distance;
        if (bAngDiamProvidedInRadians)
        {
            distance = 0.5f * actualDiameter / Mathf.Sin(0.5f * angularDiameter);
        }
        else
        {
            distance = 0.5f * actualDiameter / Mathf.Sin(0.5f * degToRad(angularDiameter));
        }
        return distance;
    }

    //determines the positions of stimulus objects in array such that they appear to be the same diameter and appear spaced apart by the same angle
    Vector3[] determinePositions(GameObject[] objs, GameObject eye, float angularDiameter, float spacingAngle)
    {
        Vector3[] determinedPositions = new Vector3[objs.Length];

        float fixedHeight = eye.transform.position.y;

        for (int i = 0; i < objs.Length; i++)
        {
            Vector3 calculatedPos = new Vector3();
            calculatedPos.y = fixedHeight; //the y position of each stimulus center is fixed at the eye height

            //retrieve the actual diameter of the stimulus sphere
            float actualDiameter = 2 * objs[i].GetComponent<SphereCollider>().radius * objs[i].transform.lossyScale.x;

            //determine the distance from the eye at which the diameter appears to be the desired angular diameter
            float distance = distFromAngDiam(angularDiameter, actualDiameter, false);

            //determine the x and z offsets (opposite and adjacent sides of right triangle) that are necessary to produce that distance

            //this is derived from the right triangle, solving for an opposite side length given an angle and a hypotenuse
            float xOffsetUnitForGivenDist = distance * Mathf.Sin(degToRad(spacingAngle));
            //the x offset will be a multiple of the desied spacing... as the center object will be offset by 0, and the left by +x and right by -x
            float xOffset = (Mathf.Floor(objs.Length / 2) - i) * xOffsetUnitForGivenDist;
            calculatedPos.x = eye.transform.position.x + xOffset;


            //the z offset will be the adjacent side of a right triangle now that we know the hypotenuse and the opposite side length
            float zOffset = Mathf.Sqrt(Mathf.Pow(distance, 2) + Mathf.Pow(xOffset, 2)); //triangle side length
            calculatedPos.z = eye.transform.position.z - zOffset;

            determinedPositions[i] = calculatedPos;
        }

        return determinedPositions;
    }

    //assigns pre-determined positions to an array of objects
    void assignPositions(GameObject[] objs, Vector3[] assignments)
    {
        for (int i = 0; i < objs.Length; i++)
        {
            objs[i].transform.position = assignments[i];
        }
    }

    //shows all the stimulus objects from an array of stimulus objects
    IEnumerator showStimuli(GameObject[] objs)
    {
        //for each stimulus going left -> right, wait 3 seconds between each display
        foreach (GameObject obj in objs)
        {
            yield return new WaitForSeconds(3.0f);
            obj.SetActive(true);
        }
        bSeqInProgress = false;
        print("main sequence complete");
    }

    //shuffles an array, useful for randomizing 
    public static void ShuffleArray<T>(T[] array)
    {
        for (int i = array.Length - 1; i > 0; i--)
        {
            int randIndex = Random.Range(0, i);
            T tmp = array[i];
            array[i] = array[randIndex];
            array[randIndex] = tmp;
        }
    }
}
```