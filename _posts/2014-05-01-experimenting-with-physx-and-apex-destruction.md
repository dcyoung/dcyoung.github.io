---
title: "Experimenting with PhysX and APEX Destruction"
date: 2014-05-01T00:00:00-00:00
last_modified_at: 2014-05-01T00:00:00-00:00
categories:
  - game dev
  - unreal engine
  - 3D
permalink: /post-experimenting-with-physx-apex/
classes: wide
toc: true
excerpt: A completely custom networked implementation of a card game called set.
header:
  og_image: /images/experimenting-with-physx-apex/3.jpg
  teaser: /images/experimenting-with-physx-apex/3.jpg
---

![example](/images/experimenting-with-physx-apex/3.jpg){:.align-center}

> The experiments here were conducted using unreal engine version 4.9.2. The content should be the same for all engine versions 4.8 -> 4.9.X. I have not tested beyond that.

## Why I like PhysX

People are curious by nature, and if you give them a world constrained by physical laws they will attempt to explore the boundaries of those constraints. It is my belief that real-time simulation will rule the future of video games and similar interactive experiences. Unscripted sandbox moments provide endless hours of entertainment unlike their un-recyclable narrative cutscene counterparts, for a world is only as immersive as it is interactive.

Many studios have aimed to incorporate elements of the PhysX toolbox into larger narrative experiences found in AAA games. I’d like to see smaller demos that are built from the ground up exclusively to demonstrate the capabilities of tools such as APEX or FLEX. Armed with a back-end physics engine, I experimented with the early mechanics of a very simple game to highlight real-time destruction.

## Creating Destructible Assets

### Prior Experience

I started experimenting with destructible assets in UE4 back in June 2014. At that time, the engine (version 4.1) provided very little in the way of support for destructible assets. A single voroni fracture tool and a few checkable settings were about all that UE4 offered internally. Because of this I turned to 3rd party tools to handle the creation of the destructible assets themselves. These tools enabled interesting fracture patterns as well as complex attributes like multiple depth levels, internal support or debris. I experimented a fair bit with PhysXLab which supplied a solid amount of functionality at an easier learning curve and a much nicer price tag (free) than some more professional VFX tools. For example, splintered wood planks were easy to generate using PhysXLab. A few combinations of sinusoids could create the splintering effects along user specified axes while levels of destruction could help define subsequent splinters. However for the more complex destructible assets I enjoyed experimenting with RayFire. Rayfire is an expensive 3DsMax and Maya plugin mostly intended for VFX in film. In combination with the physics engines supplied in Autodesk’s softwares, RayFire can produce very realistic looking fracture patterns using a wealth of tools that go beyond voroni fracture. Unfortunately I was only able to experiment with the RayFire plugin on a university lab computer which I had limited access to, so PhysXLab handled most of the work by default.

### Adopted Pipeline

To create destructible environments, I have adopted the following pipeline:

- Create 3D model of object using modelling software (my preference is Maya)
- Create multi-layered fracture patterns for the meshes using RayFire plugin or PhysXLab
- Import the fractured meshes into UE4 as destructible assets
- Build structures/environments from instances of those destructible assets

## Using Rigid Body PhysX in Code Project

### Getting PhysX Working in a UE4 Code Project

Although UE4 has APEX handle the destruction of pre-fractured meshes by default, this doesn’t provide the designer any power to experiment with behaviors beyond the basic settings of the destructible meshes. To produce more interesting behavior, I’ve tried to get up to speed quickly with the Rigid Body Dynamics of the PhysX API, as those are arguably the most useful in prototyping destruction. The first trick was getting PhysX working in a code project. Luckily some kind people before me (Rama) documented a few of the "gotchas" that saved me a lot of time with my early experimentation. These "gotchas" include the essential include, and the modifications to Build.cs.

```csharp
#include "PhysXIncludes.h" //Cannot forget this include!!!!
```

```csharp
PublicDependencyModuleNames.AddRange(new string[] {
  "Core", "CoreUObject", "Engine", "InputCore", "PhysX", "APEX" 
});
```

### Manipulating Chunks Directly

As mentioned before, creating interesting behavior is easier when its possible to work on chunks of a destructible mesh directly. Once PhysX is accessible in a coding project, this becomes simple. The basic outline of my custom destructible meshes is shown below.

```cpp
#include "FirstProjectTest.h"
#include "MyStaticLibrary.h"
#include "MyDestructibleActor.h"
//~~~~~~~~~~~~~~~~~~~~~~~~
//	   PhysX 			
#include "PhysXIncludes.h" 
//~~~~~~~~~~~~~~~~~~~~~~~~

AMyDestructibleActor::AMyDestructibleActor(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	//have to switch ticking on for this actor
	PrimaryActorTick.bCanEverTick = true; //this won't tick by default
}

//Tick
void AMyDestructibleActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	//Draw All Centers to the screen!
#if WITH_PHYSX
	//UMyStaticLibrary::ScreenMsg("Got into PhysX!!!");

	PxVec3 PxTargetLoc = PxVec3(MainCharacter->TargetPoint.X, MainCharacter->TargetPoint.Y, MainCharacter->TargetPoint.Z);

	uint32 ChunkCount = GetDestructibleComponent()->ApexDestructibleActor->getNumVisibleChunks();
	//UMyStaticLibrary::ScreenMsg("Chunk count: " + FString::FromInt(ChunkCount));
	const uint16* ChunkIndices = GetDestructibleComponent()->ApexDestructibleActor->getVisibleChunks();
	for (uint32 c = 0; c < ChunkCount; c++)
	{
		//PActor is a chunk
		PxRigidDynamic* PActor = GetDestructibleComponent()->ApexDestructibleActor->getChunkPhysXActor(ChunkIndices[c]);
		check(PActor);
		PxTransform Trans = PActor->getGlobalPose();
		PxVec3& PxLoc = Trans.p;
		
		//Very poor test to see if the mesh has broken apart yet.
		if (GetDestructibleComponent()->IsActive()){
			FVector Location(PxLoc.x, PxLoc.y, PxLoc.z);
			DrawPoint(Location);
			UMyStaticLibrary::ScreenMsg("physx loc: " + Location.ToString());
		}
	}


#endif // WITH_PHYSX
}
```

## Basic Rigid Body Dynamics

### Applying Simple Forces in Interesting Ways (Move Chunks by Aiming your Gun)

This simple test project involved changes to the character class as well as the custom destructible class. I setup a line-trace on the onFire() function in the character class. If the player tries to fire the gun, this line trace searches for an impact along the vector pointing out of the players gun. If it encounters any object, it will determine the location of impact and hold it in a public targetPoint variable.

Add the target point variable to FirstProjectTestCharacter.h...

```cpp
/** Target Point. */
UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	FVector TargetPoint;
UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = Camera)
	bool TargetPointSet;
```
Add the following bit of code for a custom trace to the OnFire() method in FirstPersonTestCharacter.cpp...

```cpp
void AFirstProjectTestCharacter::OnFire()
{ 
	// try and fire a projectile
	...
	
	//Custom Trace
	APlayerController* PC = GetWorld()->GetFirstPlayerController();
	const FVector Start = PC->GetFocalLocation();
	const FVector End = Start + PC->GetControlRotation().Vector() * 5000;
	FHitResult HitData(ForceInit);
	//If Trace Hits anything (ignore the controlled pawn)
	if (UMyStaticLibrary::Trace(GetWorld(), PC->GetPawn(), Start, End, HitData, COLLISION_WEAPON, false) && HitData.GetActor())
	{
		UMyStaticLibrary::ScreenMsg(HitData.GetActor()->GetName());

		TargetPoint = HitData.ImpactPoint;
		TargetPointSet = true;

		//Print out the distance from the trace start to the impact point!
		UMyStaticLibrary::ScreenMsg("Distance from Trace Start to Impact: " + FString::SanitizeFloat(HitData.Distance));
	}
}
```

In my static library class, where I hold many useful functions to be called from any class, the trace method is as follows...

```cpp
```

In my custom destructible class I have setup a basic tick function. If the destructible breaks apart into chunks, the chunks will be flung toward whatever location the player specifies with his/her gun. The parameters specifying the force magnitude and type (impulse or velocity change) can be specified via blueprints and even changed at run time.

```cpp
// MyDestructibleActor.h ...
#pragma once
#include "PhysicsEngine/DestructibleActor.h"
#include "Engine.h"
#include "FirstProjectTestCharacter.h"
#include "MyDestructibleActor.generated.h"
UCLASS()
class AMyDestructibleActor : public ADestructibleActor
{
	GENERATED_UCLASS_BODY()

protected:
	virtual void Tick(float DeltaTime) override;
public:
	//Drawing!
	FORCEINLINE void DrawPoint
		(
		const FVector& Loc,
		const float& Size = 7,
		const FColor& Color = FColor::Red,
		const float Duration = -1.f
		) const {
		DrawDebugPoint(
			GetWorld(),
			Loc,
			Size, //thickness
			Color,
			false,
			Duration
			);
	}
	
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Force Response")
	float ForceScale;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Force Response")
	bool bUseImpulse;

private:
	AFirstProjectTestCharacter* MainCharacter;
};
```

```cpp
// MyDestructibleActor.cpp
#include "FirstProjectTest.h"
#include "MyStaticLibrary.h"
#include "MyDestructibleActor.h"
//~~~~~~~~~~~~~~~~~~~~~~~~
//	   PhysX 			
#include "PhysXIncludes.h" 
//~~~~~~~~~~~~~~~~~~~~~~~~

AMyDestructibleActor::AMyDestructibleActor(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
	//have to switch ticking on for this actor
	PrimaryActorTick.bCanEverTick = true; //this won't tick by default
	//MainCharacter = Cast(GetWorld()->GetFirstPlayerController()->GetCharacter());
	ForceScale = 0.15; //
	bUseImpulse = true;
}

//Tick
void AMyDestructibleActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
	//~~~~~~~~~~~~
	if (!UMyStaticLibrary::IsValid(MainCharacter)){
		MainCharacter = Cast(GetWorld()->GetFirstPlayerController()->GetCharacter());
	}

	//Draw All Centers to the screen!
#if WITH_PHYSX
	//UMyStaticLibrary::ScreenMsg("Got into PhysX!!!");

	if (MainCharacter->TargetPointSet){

		PxVec3 PxTargetLoc = PxVec3(MainCharacter->TargetPoint.X, MainCharacter->TargetPoint.Y, MainCharacter->TargetPoint.Z);

		uint32 ChunkCount = GetDestructibleComponent()->ApexDestructibleActor->getNumVisibleChunks();
		//UMyStaticLibrary::ScreenMsg("Chunk count: " + FString::FromInt(ChunkCount));
		const uint16* ChunkIndices = GetDestructibleComponent()->ApexDestructibleActor->getVisibleChunks();
		for (uint32 c = 0; c < ChunkCount; c++)
		{
			//PActor is a chunk
			PxRigidDynamic* PActor = GetDestructibleComponent()->ApexDestructibleActor->getChunkPhysXActor(ChunkIndices[c]);
			check(PActor);
			PxTransform Trans = PActor->getGlobalPose();
			PxVec3& PxLoc = Trans.p;
			
			//Very poor test to see if the mesh has broken apart yet.
			if (GetDestructibleComponent()->IsActive()){
				PActor->clearForce(physx::PxForceMode::eVELOCITY_CHANGE);
				PActor->clearForce(physx::PxForceMode::eIMPULSE);
				PxVec3 PxTowardTarget = PxVec3(PxTargetLoc.x - PxLoc.x, PxTargetLoc.y - PxLoc.y, PxTargetLoc.z - PxLoc.z);
				if (bUseImpulse)
				{
					PActor->addForce(ForceScale*PxTowardTarget, physx::PxForceMode::eIMPULSE);
				}
				else
				{
					PActor->addForce(ForceScale*PxTowardTarget, physx::PxForceMode::eVELOCITY_CHANGE);
				}
			}

			FVector Location(PxLoc.x, PxLoc.y, PxLoc.z);

			DrawPoint(Location);
			//UMyStaticLibrary::ScreenMsg("physx loc: " + Location.ToString());
		}
	}

#endif // WITH_PHYSX
}
```

Controlling a swarm of chunks this way is very entertaining, and might also have real game applications. I could see this type of setup controlling swarms of bees or birds like in bio-shock infinite, or stopping and redirecting a barrage of bullets and artillery similar to scenes from X-Men.

<figure class="half">
  <img src="/images/experimenting-with-physx-apex/0.jpg">
  <img src="/images/experimenting-with-physx-apex/1.jpg">
</figure>

<figure class="half">
  <img src="/images/experimenting-with-physx-apex/2.jpg">
  <img src="/images/experimenting-with-physx-apex/3.jpg">
</figure>

### Experimenting with Other Uses:

Since these dynamics are updated every tick, things can easily be parameterized with respect to the tick count. I’m sure there exist easy ways to do the same with global delta-time stamp from the game instance, but this worked for early experimentation. In theory, all one needs to create interesting behavior for the movement of chunks is the parametric equations for the desired movement patterns. Most movements devolve into simpler equations, combinations of sinusoids etc. The trickier part comes in tweaking the parameters used the equations to produce a natural looking effect. I found using real-world values did not equate to real-looking results.

```cpp
/*----------FOR AN Oscillating/BOUNCING EFFECT----------*/
PxVec3& oscillateVec = Trans.p;
oscillateVec.x = 0;
oscillateVec.y = 0;
oscillateVec.z = A*sin(w*t);
chunk->addForce(oscillateVec, physx::PxForceMode::eVELOCITY_CHANGE);
```

```cpp
/*-------------For A Circular or Helix Effect:----------------
Think Torandos and Dust-Devils, Or Trash/Leaves circling in the wind.
these are actually the eqns for pos, and will have undesireable
behavior when used as force or velocity vectors. Although simply
calculating the derivatives w.r.t "tick count" should yield natural
results, in my brief experimentation, simply tweaking different
parameters yielded better resutls.
*/
PxVec3& forceVec = Trans.p;
forceVec.x = radius*cos(w*t);
forceVec.y = radius*sin(w*t);
forceVec.z = 0;
chunk->addForce(forceVec, physx::PxForceMode::eVELOCITY_CHANGE);

// or...
PxVec3& torqueVec = Trans.p;
torqueVec.x = 0;
torqueVec.y = 0;
torqueVec.z = 100;
chunk->addTorque(torqueVec, physx::PxForceMode::eVELOCITY_CHANGE);
```

```cpp
/*------------Helix Effect (use velocity)----------*/
PxVec3& helixVelocity = Trans.p;
helixVelocity.x = -w * radius*sin(w*t);
helixVelocity.y = w * radius*cos(w*t);
helixVelocity.z = desiredZvelocity;
chunk->setAngularVelocity(scale*helixVelocity, true);
//unclear on how the system interprets ang. and linear vel... as neither seem natural without tweaking.
```
