# Unity ECS 

- [Code Monkey ECS RTS game](https://www.youtube.com/watch?v=1gSnTlUjs-s)

## Code monkey Tutorial notes

- [Code Monkey 1h ECS Extreme Performance](https://www.youtube.com/watch?v=4ZYn9sR3btg)


### Questions 

- [ ] `SystemAPI` usecases commands 
- [ ] `SystemAPI.Query` usecases commands
- [ ] EnityCommandBuffer usecases commands
- [ ] `entityManager` usecases commands


### Getting started with Unity ECS

1. Do not reload domain
![[Pasted image 20250812071238.png]]
2. Add Entities package
![[Pasted image 20250812074053.png]]

- Entities 
- Entities Graphics
- Mathematics
- Collections
- Burst 

3. Creating Entity subscene

`Create` > `New subscene` > `Empty scene`

### Entities hierarchy 

`Window` > `Entities` > `Hierarchy`

![[Pasted image 20250812103741.png]]

### Entities Code 

#### IComponentData

`IComponentData` is used to define data components in Unity ECS. These components are used to store data for entities.

```csharp
using Unity.Entities;

public struct RotationSpeed : IComponentData
{
    public float Value; 
} 
```

#### MonoBehaviour - Baker

`Baker` - is used to convert `MonoBehaviour` data into ECS components. 
`AddComponent` - is used to add a component to an entity.

```csharp
using Unity.Entities;
using UnityEngine;

public class RotationSpeedAuthoring: MonoBehaviour
{
     public float value; 
    private class Baker : Baker<RotationSpeedAuthoring>
    {
        public override void Bake(RotationSpeedAuthoring authoring)
        {
            Entity entity =  GetEntity(TransformUsageFlags.Dynamic);
            var rs = new RotationSpeed { Value = authoring.value };
            AddComponent(entity,rs);
        }
    } 
} 

```
#### SystemBase vs ISystem

`SystemBase` - is a base class for creating systems in Unity ECS. It provides a way to define the behavior of entities. `class`

`ISystem` - is an interface for creating systems in Unity ECS. It's compitable with Burst compiler and is more performant. `struct`

`SystemBase` allows to store references to entities, while `ISystem` does not. 
`ISystem` is **Burst compatible** and is more performant than `SystemBase`. 

##### Basic ISystem struct 

```csharp
using Unity.Entities;
using Unity.Transforms;

public partial struct RotationCubeSystem: ISystem
{
    public void OnCreate(ref SystemState state) { } 
    public void OnUp(ref SystemState state) { }
    public void OnDestroy(ref SystemState state){ } 
}
```

- `OnUpdate()` - is called every frame and is used to **update** the system.
- `OnCreate()` - is called when the system is created and is used to **initialize** the system.
- `OnDestroy()` - is called when the system is destroyed and is used to **clean up** the system.

##### Simple rotation system

```csharp
using Unity.Entities;
using Unity.Transforms;

public partial struct RotationCubeSystem: ISystem
{
    public void OnUpdate(ref SystemState state)
    {
         foreach (var (localTransform, rotationSpeed) 
                  in SystemAPI.Query<RefRW<LocalTransform>,RefRO<RotationSpeed>>()) {
             
             localTransform.ValueRW = localTransform.ValueRO.RotateY(rotationSpeed.ValueRO.Value*SystemAPI.Time.DeltaTime); 
         }
    } 
}
```

##### Disabling a system

```csharp
public void OnUpdate(ref SystemState state){

    state.Enabled = flase;
return;
/*
...
*/
```

#### RerRO vs RefRW or Reference wrappers

Reference wrappers are used incide ECS queries to safely and efficiently access component data.

- `RefRO` - is used to read data from an entity. It is a **read-only** reference to the data.
- `RefRW` - is used to read and write data to an entity. It is a **read-write** reference to the data.



```csharp
foreach ( var (pos,speed) in SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeed>>())
{
    pos.ValueRW.Rotation = math.mul(pos.ValueRW.Rotation, quaternion.RotateY(speed.ValueRO.Value * SystemAPI.Time.DeltaTime)); }
```

Writing with RefRW and reading with RefRO is more performant than using `GetComponentData()` and `SetComponentData()`.

Reading/Writing without them would not change the entity value.

#### Mathematics 

`math.mul()` - is used to multiply two quaternions.


#### System Registration

```csharp
public partial struct RotationCubeSystem: ISystem
{
    public void OnCreate(ref SystemState state)
    {
        state.RequireForUpdate<RotationSpeed>(); 
    }

```

#### Burst Compilation

To enable Burst compilation, you need to add the `BurstCompile` attribute to your system. 

![[Pasted image 20250812174815.png]]

If you use `class` anywhere the Burst compilation will not work.

```csharp

    
    [BurstCompile]
    public void OnUpdate(ref SystemState state) 
    {
    }
```

#### Jobs 


##### Job Syntaxis 

```csharp

    public  partial struct RotationCubeJob : IJobEntity
    {
        public float deltaTime;
        public void Execute(ref LocalTransform localTransform, ref RotationSpeed rotationSpeed)
        {
            float power = 1f;
            for (int i = 0; i < 100000; i++)
            {
                power *= 2f;
                power /= 2f;
            }
             
            localTransform = localTransform.RotateY(rotationSpeed.Value*deltaTime*power); 
        }
    }


```

###### Sheduling a Job

```csharp
//short hand 
job.Schedule(); //instead of job.Run()

//actual implementation
state.Dependency = job.Schedule(state.Dependency); //If you want to use dependencies
```


```csharp
    [BurstCompile]
    public void OnUpate(ref SystemState state)
    {
        var job = new RotationCubeJob
        {
            deltaTime = SystemAPI.Time.DeltaTime
        }
        /*job.Run();*/
        job.Schedule();
    }

    public void OnUpdate(ref SystemState state) 
    {
        var job = new RotationCubeJob
        {
            deltaTime = SystemAPI.Time.DeltaTime
        };
        job.Schedule(); 
    }
```

##### IJobEntity vs IJob

`IJobEntity` - automatically iterates over entities and provides access to their components.
`IJob` - requires you to manually iterate over entities and provides access to their components.

#### Tag Components  

Tag component is `IComponentData` that does not contain any data.

```csharp
public struct MyTag : IComponentData { } //tag component 

```
##### With None 

The following code will run the only for entities that do not have the `MyTag` component.

```csharp
[WithNone(typeof(MyTag))]
public  partial struct RotationCubeJob : IJobEntity 

```
> Actual implementation : 

```csharp
SystemAPI.Query<RefRW<LocalTransform>,RefRO<RotationSpeed>>().WithNone<PlayerTag>()
```


#### Mathematics

`float3` - is a 3D vector that contains three float values (x, y, z).
`float2` - is a 2D vector that contains two float values (x, y).
`quaternion` - is a mathematical representation of rotation in 3D space.
`math` - is a static class that contains various mathematical functions and constants.

```csharp
float3 position = new float3(1f, 2f, 3f);
float2 uv = new float2(0.5f, 0.5f);
quaternion rotation = quaternion.EulerXYZ(new float3(0f, math.radians(90f), 0f));
float length = math.length(position);
float dotProduct = math.dot(new float3(1f, 0f, 0f), new float3(0f, 1f, 0f));
```

#### Aspects (iAspect)

`IAspect` is a way to define a group of entity data that will be used together.

> ❗️**IAspect** is used with `readonly` and `struct` 

##### IAspect usecase

Converting from:

```csharp
foreach ((RefRW<LocalTransform> localTransform, RefRO<RotationSpeedData> rotationSpeed,RefRO<MovementData> movement) in 
         SystemAPI.Query<RefRW<LocalTransform>,RefRO<RotationSpeedData>,RefRO<MovementData>>().WithAll<RotatingCubeTag>())
```
Converting into:

```csharp
foreach (var aspect in SystemAPI.Query<RotationAspect>())
{
    aspect.Rotate(SystemAPI.Time.DeltaTime);
}
```

###### IAspect Example

```csharp
using Unity.Entities;

public readonly partial struct RotationAspect : IAspect{
    public readonly RefRO<LocalTransform> LocalTransform;
    public readonly RefRO<RotationSpeed> RotationSpeed;
    public float RotationSpeedValue => RotationSpeed.ValueRO.Value;
 
    public void Rotate(float deltaTime)
    {
        var rotation = quaternion.EulerXYZ(0,RotationSpeedValue*deltaTime,0); 
        LocalTransform.ValueRW.Rotation = math.mul(LocalTransform.ValueRO.Rotation,rotation);
    }
}
```

#### Entity 

`Entity` is a struct that represents an entity in Unity ECS. It is used to create, destroy, and manage entities. Contains ID and version.
> is like `GameObject` in Unity, but without any components.

##### Creating an Entity

- `SystemAPI.EntityManager.CreateEntity()` - is used to create and manage entities in Unity ECS.

```csharp
entity = SystemAPI.EntityManager.CreateEntity();
entityManager.AddComponentData(entity, new Transform { Position = new float3(0, 0, 0) });
entityManager.AddComponentData(entity, new Rotation { Value = quaternion.identity });
```

##### Instantiating an Entity

- `EntityManager.Instantiate()` is used to create a new entity from a prefab entity.

```csharp
Entity entity = SystemAPI.EntityManager.Instantiate(prefabEntity);
````

##### Getting and Entity 

We can use `GetEntity` method inside a `Baker` class to get the entity associated with a `MonoBehaviour`.

```csharp
Entity entity = GetEntity(TransformUsageFlags.Dynamic);
```
###### TransformUsageFlags

`TransformUsageFlags` - is an enum that defines how the transform of an entity will be used.

- `Dynamic` - is used for entities that will be moved or rotated frequently.
- `None` - The entity will not have a transform.
- `WorldSpace` - entitys position is set in world cordinates.

###### Getting an Entity from a GameObject

```csharp
Entity entity = GetEntity(authoring.gameObject, TransformUsageFlags.Dynamic);
```

##### Singelton Entity 

A singleton entity is an entity that has only one instance in the world. It is used to store global data that is shared across all entities.

- `RequireSingletonForUpdate<SpawnnCubesSingleton>()` - is used to require singleton to be present.
- `SystemAPI.GetSingleton<SpawnnCubesSingleton>()` - is used to get the singleton entity.
- `SystemAPI.SetSingleton<SpawnnCubesSingleton>(value)` - is used to set the singleton entity .


```csharp

public struct SpawnnCubesSingleton : IComponentData
{
    public int Count;
}

public partial struct SpawnCubesSystem : ISystem
{
    public void OnCreate(ref SystemState state)
    {
        state.RequireSingletonForUpdate<SpawnnCubesSingleton>();
    }
    public void OnUpdate(ref SystemState state)
    {
        config = SystemAPI.GetSingleton<SpawnnCubesSingleton>();
        config.Count++;
        SystemAPI.SetSingleton<SpawnnCubesSingleton>(config);

    }
}

```

#### EntityCommandBuffer (ECB)

**EntityCommandBuffer (ECB)** is a way to record structural changes to entities and apply them later. It allows you to safely modify entities from jobs or other systems without immediately affecting the entity manager.

EntityCommandBuffer fixed my shit code now it's working correctly.

You also use instead of `state.EntityManager` to modify entities. for instance set position, rotation, etc.
**Syntaxis:**
`BeginInitializationEntityCommandBufferSystem.Singleton.CreateCommandBuffer(state.WorldUnmanaged);`

##### Without ECS



```csharp

public partial struct SpawnNoECBSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var spawner = SystemAPI.GetSingleton<Spawner>();
        var entities = state.EntityManager.Instantiate(spawner.Prefab, spawner.Count, Allocator.Temp);
    }
}
```

##### With ECB 

```csharp
public partial struct SpawnWithECBSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var ecb = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>().CreateCommandBuffer(state.WorldUnmanaged);
        var spawner = SystemAPI.GetSingleton<Spawner>();
        for (int i = 0; i < spawner.Count; i++)
            ecb.Instantiate(spawner.Prefab);
            ecb.SetComponent(spawner.Prefab, new LocalTransform { Position = new float3(0, 0, 0), Rotation = quaternion.identity });
}
}

```


#### IEnableableComponent

`IEnableableComponent` is an interface that allows you to enable or disable an entity. It is used to control the behavior of entities in Unity ECS.

**❗️ Not a structural change** - it does not change the entity structure, but rather changes the state of the entity.

##### Enabling and Disabling an Entity

```csharp

public partial struct EnableDisableSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var query = SystemAPI.QueryBuilder().WithAll<EnableableComponent>().Build();
        foreach (var entity in query)
        {
            if (/* some condition */)
            {
                SystemAPI.SetComponentEnabled<EnableableComponent>(entity, true);
            }
            else
            {
                SystemAPI.SetComponentEnabled<EnableableComponent>(entity, false);
            }
        }
    }
}
```


### Query 

Here’s a Markdown explanation of Query in Unity ECS with the most used methods and calls.

⸻

🔍 SystemAPI.Query in Unity ECS

SystemAPI.Query is used inside SystemBase or ISystem to iterate over entities that match specific component types and filters.
It’s a type-safe, Burst-friendly way to access components without manually writing Entities.ForEach.

⸻

Basic Usage

foreach (var (transform, velocity) in 
         SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>())
{
    // transform is writable, velocity is read-only
}


⸻

📜 Common Component Access Modifiers

Modifier	Meaning	Example
RefRO<T>	Read-only access to component T	RefRO<Health>
RefRW<T>	Read-write access to component T	RefRW<LocalTransform>
EnabledRefRO<T>	Read-only access for enabled/disabled components	EnabledRefRO<MyTag>
EnabledRefRW<T>	Read-write access for enabled/disabled components	EnabledRefRW<MyTag>


⸻

⚙ Filtering Methods

1. .WithAll<T>()

Selects entities that have all of the listed components or tags.

SystemAPI.Query<RefRO<Health>>()
         .WithAll<PlayerTag, AliveTag>();


⸻

2. .WithAny<T>()

Selects entities that have at least one of the listed components.

SystemAPI.Query<RefRO<Health>>()
         .WithAny<ZombieTag, VampireTag>();


⸻

3. .WithNone<T>()

Excludes entities with specific components.

SystemAPI.Query<RefRO<Health>>()
         .WithNone<DeadTag>();


⸻

4. .WithEntityAccess()

Gives you access to the entity ID in the loop.

foreach ((var transform, var entity) in 
         SystemAPI.Query<RefRO<LocalTransform>>()
                  .WithAll<PlayerTag>()
                  .WithEntityAccess())
{
    // entity is the Entity struct
}


⸻

5. .WithDisabled<T>()

Includes entities where component T is disabled.

SystemAPI.Query<RefRW<AIState>>()
         .WithDisabled<AIEnabled>();


⸻

🛠 Special Cases

Getting a Single Component

var playerHealth = SystemAPI.GetSingleton<Health>();

var ecb = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                   .CreateCommandBuffer(World.Unmanaged);


⸻

Accessing Lookups

Lookups allow random access to component data outside of direct queries.

var transformLookup = SystemAPI.GetComponentLookup<LocalTransform>(isReadOnly: false);


⸻

🚀 Performance Tips
	•	Use RefRO unless you need to modify — this allows Burst optimizations.
	•	Chain filters to reduce the number of entities processed.
	•	Use `.WithEntityAccess()` only if you really need the entity ID.

⸻

