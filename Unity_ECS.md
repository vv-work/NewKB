# Unity ECS (Entity Component System)

Unity ECS is a data-oriented design pattern that provides high performance and enables massive parallelization through the Burst compiler and Job System.

## Resources

- [Code Monkey ECS RTS game](https://www.youtube.com/watch?v=1gSnTlUjs-s)
- [Code Monkey 1h ECS Extreme Performance](https://www.youtube.com/watch?v=4ZYn9sR3btg)

## Setup and Configuration

### Initial Setup

1. **Disable Domain Reloading**
   ![[Pasted image 20250812071238.png]]

2. **Install Required Packages**
   ![[Pasted image 20250812074053.png]]
   - Entities 
   - Entities Graphics
   - Mathematics
   - Collections
   - Burst 

3. **Create Entity Subscene**
   `Create` > `New subscene` > `Empty scene`

### Entities Hierarchy Window

Access via: `Window` > `Entities` > `Hierarchy`
![[Pasted image 20250812103741.png]]


## Components

### IComponentData

`IComponentData` defines data components that store information for entities. These are pure data structures without behavior.

```csharp
using Unity.Entities;

public struct RotationSpeed : IComponentData
{
    public float Value; 
} 
```

### Authoring and Baking

**Baker** converts `MonoBehaviour` data into ECS components during the baking process.

```csharp
using Unity.Entities;
using UnityEngine;

public class RotationSpeedAuthoring : MonoBehaviour
{
    public float value; 
    
    private class Baker : Baker<RotationSpeedAuthoring>
    {
        public override void Bake(RotationSpeedAuthoring authoring)
        {
            Entity entity = GetEntity(TransformUsageFlags.Dynamic);
            var rs = new RotationSpeed { Value = authoring.value };
            AddComponent(entity, rs);
        }
    } 
}
```

## Systems

### SystemBase vs ISystem

| Feature | SystemBase | ISystem |
|---------|------------|----------|
| Type | `class` | `struct` |
| Burst Compatible | ❌ | ✅ |
| Performance | Lower | Higher |
| Can store references | ✅ | ❌ |
| Memory allocation | Higher | Lower |

**Recommendation**: Use `ISystem` for performance-critical systems.

### Basic ISystem Structure

```csharp
public partial struct RotationCubeSystem : ISystem
{
    public void OnCreate(ref SystemState state) { } 
    public void OnUpdate(ref SystemState state) { }
    public void OnDestroy(ref SystemState state) { } 
}
```

**System Lifecycle Methods:**
- `OnCreate()` - Initialize system (called once)
- `OnUpdate()` - Process entities every frame
- `OnDestroy()` - Clean up resources (called once)

### System Examples

**Simple Rotation System:**

```csharp
using Unity.Entities;
using Unity.Transforms;

public partial struct RotationCubeSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (localTransform, rotationSpeed) 
                 in SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeed>>()) 
        {
            localTransform.ValueRW = localTransform.ValueRO.RotateY(
                rotationSpeed.ValueRO.Value * SystemAPI.Time.DeltaTime
            ); 
        }
    } 
}
```

**Disabling a System:**

```csharp
public void OnUpdate(ref SystemState state)
{
    state.Enabled = false;
    return;
    // Rest of system logic...
}
```

## Reference Wrappers

Reference wrappers provide safe and efficient access to component data in ECS queries.

| Wrapper | Access | Usage |
|---------|--------|---------|
| `RefRO<T>` | Read-only | `RefRO<RotationSpeed>` |
| `RefRW<T>` | Read-write | `RefRW<LocalTransform>` |
| `EnabledRefRO<T>` | Read-only enabled components | For IEnableableComponent |
| `EnabledRefRW<T>` | Read-write enabled components | For IEnableableComponent |

**Example Usage:**
```csharp
foreach (var (pos, speed) in SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeed>>())
{
    pos.ValueRW.Rotation = math.mul(
        pos.ValueRW.Rotation, 
        quaternion.RotateY(speed.ValueRO.Value * SystemAPI.Time.DeltaTime)
    );
}
```

**Performance Benefits:**
- More performant than `GetComponentData()` and `SetComponentData()`
- Type-safe access with compile-time checks
- Burst-compatible for maximum performance



### System Requirements

```csharp
public partial struct RotationCubeSystem : ISystem
{
    public void OnCreate(ref SystemState state)
    {
        state.RequireForUpdate<RotationSpeed>(); 
    }
}
```


### Component Types

#### Tag Components  

Tag components are `IComponentData` without data, used purely for identification and filtering.

```csharp
public struct PlayerTag : IComponentData { }
public struct EnemyTag : IComponentData { }
public struct DeadTag : IComponentData { }
```

#### Filtering with Tags

**Job-based filtering:**
```csharp
[WithNone(typeof(DeadTag))]
public partial struct RotationCubeJob : IJobEntity 
{
    // Only processes entities without DeadTag
}
```

**Query-based filtering:**
```csharp
// Exclude entities with PlayerTag
SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeed>>()
         .WithNone<PlayerTag>()
```


## Mathematics 

### Structs 

Unity Mathematics provides Burst-compatible math types and functions.

**Core Types:**
- `float2` - 2D vector (x, y)
- `float3` - 3D vector (x, y, z)  
- `float4` - 4D vector (x, y, z, w)
- `quaternion` - Rotation representation
- `float4x4` - Transformation matrix

**Common Operations:**
```csharp
float3 position = new float3(1f, 2f, 3f);
float2 uv = new float2(0.5f, 0.5f);
quaternion rotation = quaternion.EulerXYZ(0f, math.radians(90f), 0f);

// Vector operations
float length = math.length(position);
float dotProduct = math.dot(new float3(1f, 0f, 0f), new float3(0f, 1f, 0f));
float3 normalized = math.normalize(position);
float distance = math.distance(float3.zero, position);

// Quaternion operations
quaternion rotY = quaternion.RotateY(math.radians(45f));
math.mul(rotation, rotY); // Combine rotations
```

### Methods 
•	**Dot product (·):** “How aligned?” → 📏 Number (scalar)
•	**Cross product (×):** “What’s the perpendicular spin?” (oreintation) → 🧭 Vector

`math.mul()` - is used to multiply two quaternions.
`math.lerp()` - is used to linearly interpolate between two values.

`math.dot()` - is used to calculate the dot product of two vectors.
`math.cross()` - is used to calculate the cross product of two vectors.

`math.radians()` - is used to convert degrees to radians.
`math.degrees()` - is used to convert radians to degrees.

`math.normalize()` - is used to normalize a vector.
`math.length()` - is used to get the length of a vector.

```csharp
quaternion rotation = quaternion.EulerXYZ(0f, math.radians(90f), 0f);
quaternion rotY = quaternion.RotateY(math.radians(45f));
quaternion combinedRotation = math.mul(rotation, rotY);

float3 positionA = new float3(1f, 2f, 3f);
float3 positionB = new float3(4f, 5f, 6f);

float distance = math.distance(positionA, positionB);
float3 direction = math.normalize(positionB - positionA);
float dotProduct = math.dot(new float3(1f, 0f, 0f), new float3(0f, 1f, 0f));
float3 crossProduct = math.cross(new float3(1f, 0f, 0f), new float3(0f, 1f, 0f));
```

## Aspects

`IAspect` groups related component data into a cohesive interface, improving code organization and reusability.

**Requirements:**
- Use `readonly partial struct`
- Implement `IAspect` interface
- Define component references as fields

**Before (verbose query):**
```csharp
foreach (var (localTransform, rotationSpeed, movement) in 
         SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeedData>, RefRO<MovementData>>()
                  .WithAll<RotatingCubeTag>())
{
    // Complex logic here...
}
```

**After (clean aspect):**
```csharp
foreach (var aspect in SystemAPI.Query<RotationAspect>())
{
    aspect.Rotate(SystemAPI.Time.DeltaTime);
}
```

**Aspect Implementation:**
```csharp
using Unity.Entities;
using Unity.Transforms;
using Unity.Mathematics;

public readonly partial struct RotationAspect : IAspect
{
    readonly RefRW<LocalTransform> localTransform;
    readonly RefRO<RotationSpeed> rotationSpeed;
    
    public float RotationSpeedValue => rotationSpeed.ValueRO.Value;
 
    public void Rotate(float deltaTime)
    {
        var rotation = quaternion.RotateY(RotationSpeedValue * deltaTime);
        localTransform.ValueRW.Rotation = math.mul(
            localTransform.ValueRO.Rotation, 
            rotation
        );
    }
}
```

## Entity 

`Entity` is a struct that represents an entity in Unity ECS. It is used to create, destroy, and manage entities. Contains ID and version.
> is like `GameObject` in Unity, but without any components.

### Creating an Entity

- `SystemAPI.EntityManager.CreateEntity()` - is used to create and manage entities in Unity ECS.

```csharp
entity = SystemAPI.EntityManager.CreateEntity();
entityManager.AddComponentData(entity, new Transform { Position = new float3(0, 0, 0) });
entityManager.AddComponentData(entity, new Rotation { Value = quaternion.identity });
```

### Instantiating an Entity

- `EntityManager.Instantiate()` is used to create a new entity from a prefab entity.

```csharp
Entity entity = SystemAPI.EntityManager.Instantiate(prefabEntity);
````

### Getting and Entity 

We can use `GetEntity` method inside a `Baker` class to get the entity associated with a `MonoBehaviour`.

```csharp
Entity entity = GetEntity(TransformUsageFlags.Dynamic);
```
### TransformUsageFlags

`TransformUsageFlags` - is an enum that defines how the transform of an entity will be used.

- `Dynamic` - is used for entities that will be moved or rotated frequently.
- `None` - The entity will not have a transform.
- `WorldSpace` - entitys position is set in world cordinates.

###### Getting an Entity from a GameObject

```csharp
Entity entity = GetEntity(authoring.gameObject, TransformUsageFlags.Dynamic);
```

### Singelton Entity 

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

## IEnableableComponent

`IEnableableComponent` is an interface that allows you to enable or disable an entity. It is used to control the behavior of entities in Unity ECS.

**❗️ Not a structural change** - it does not change the entity structure, but rather changes the state of the entity.

### Enabling and Disabling an Entity

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
## EntityCommandBuffer (ECB)

**EntityCommandBuffer (ECB)** is a way to record structural changes to entities and apply them later. It allows you to safely modify entities from jobs or other systems without immediately affecting the entity manager.

EntityCommandBuffer fixed my shit code now it's working correctly.

You also use instead of `state.EntityManager` to modify entities. for instance set position, rotation, etc.

**Syntaxis:**
`BeginInitializationEntityCommandBufferSystem.Singleton.CreateCommandBuffer(state.WorldUnmanaged);`

In the end:

`ecb.PlayBack(EntityManager)`

### Without ECB

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

### With ECB 

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




