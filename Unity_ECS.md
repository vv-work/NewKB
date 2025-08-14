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

## Quick Reference Questions

- [ ] `SystemAPI` use cases and commands 
- [ ] `SystemAPI.Query` use cases and commands
- [ ] `EntityCommandBuffer` use cases and commands
- [ ] `EntityManager` use cases and commands

## Core Concepts

### Components

#### IComponentData

`IComponentData` defines data components that store information for entities. These are pure data structures without behavior.

```csharp
using Unity.Entities;

public struct RotationSpeed : IComponentData
{
    public float Value; 
} 
```

#### Authoring and Baking

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
### Systems

#### SystemBase vs ISystem

| Feature | SystemBase | ISystem |
|---------|------------|----------|
| Type | `class` | `struct` |
| Burst Compatible | ❌ | ✅ |
| Performance | Lower | Higher |
| Can store references | ✅ | ❌ |
| Memory allocation | Higher | Lower |

**Recommendation**: Use `ISystem` for performance-critical systems.

#### Basic ISystem Structure

```csharp
using Unity.Entities;
using Unity.Transforms;

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

#### System Examples

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

### Reference Wrappers

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

#### Mathematics 

`math.mul()` - is used to multiply two quaternions.


#### System Requirements

```csharp
public partial struct RotationCubeSystem : ISystem
{
    public void OnCreate(ref SystemState state)
    {
        state.RequireForUpdate<RotationSpeed>(); 
    }
}
```

### Performance Optimization

#### Burst Compilation

Burst compilation provides massive performance improvements by compiling to highly optimized native code.

![[Pasted image 20250812174815.png]]

**Requirements:**
- Use `struct` instead of `class` for systems
- Avoid managed references
- Use `ISystem` instead of `SystemBase`

```csharp
[BurstCompile]
public partial struct MySystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state) 
    {
        // High-performance system logic
    }
}
```

#### Job System

The Job System enables parallel processing of entities for maximum performance.

**Job Structure:**
```csharp
public partial struct RotationCubeJob : IJobEntity
{
    public float deltaTime;
    
    public void Execute(ref LocalTransform localTransform, ref RotationSpeed rotationSpeed)
    {
        // Expensive computation example
        float power = 1f;
        for (int i = 0; i < 100000; i++)
        {
            power *= 2f;
            power /= 2f;
        }
         
        localTransform = localTransform.RotateY(rotationSpeed.Value * deltaTime * power); 
    }
}
```

**Scheduling Jobs:**
```csharp
[BurstCompile]
public void OnUpdate(ref SystemState state)
{
    var job = new RotationCubeJob
    {
        deltaTime = SystemAPI.Time.DeltaTime
    };
    
    // Simple scheduling
    job.Schedule();
    
    // With dependency management
    // state.Dependency = job.Schedule(state.Dependency);
}
```

**Job Types Comparison:**

| Type | Description | Use Case |
|------|-------------|----------|
| `IJobEntity` | Auto-iterates over entities | Most common, entity processing |
| `IJob` | Manual iteration required | Custom logic, single operations |

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


## Mathematics Library

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

### Aspects

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

In the end:

`ecb.PlayBack(EntityManager)`

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

## Data Structures

### NativeArray

`NativeArray<T>` is a Burst-compatible array that provides safe memory management and parallel job access.

**Key Features:**
- Burst-compatible for high performance
- Memory safety with bounds checking
- Automatic memory management with `Allocator` types
- Thread-safe parallel access patterns

**Creation and Usage:**
```csharp
using Unity.Collections;

// Create NativeArray
var array = new NativeArray<float3>(100, Allocator.TempJob);

// Access elements
array[0] = new float3(1, 2, 3);
float3 value = array[0];

// Always dispose when done
array.Dispose();
```

**Allocator Types:**
```csharp
// Short-lived (within frame)
var temp = new NativeArray<int>(10, Allocator.Temp);

// Job duration
var tempJob = new NativeArray<int>(10, Allocator.TempJob);

// Persistent across frames
var persistent = new NativeArray<int>(10, Allocator.Persistent);
```

**Job System Integration:**
```csharp
[BurstCompile]
public struct ProcessArrayJob : IJob
{
    public NativeArray<float3> positions;
    public float deltaTime;
    
    public void Execute()
    {
        for (int i = 0; i < positions.Length; i++)
        {
            positions[i] += new float3(0, deltaTime, 0);
        }
    }
}

// Usage in system
public void OnUpdate(ref SystemState state)
{
    var positions = new NativeArray<float3>(entityCount, Allocator.TempJob);
    
    var job = new ProcessArrayJob
    {
        positions = positions,
        deltaTime = SystemAPI.Time.DeltaTime
    };
    
    state.Dependency = job.Schedule(state.Dependency);
    
    // Dispose after job completes
    state.Dependency.Complete();
    positions.Dispose();
}
```

**Memory Management Best Practices:**
```csharp
// Use using statement for automatic disposal
using var array = new NativeArray<int>(100, Allocator.TempJob);

// Or dispose manually
var array = new NativeArray<int>(100, Allocator.TempJob);
try
{
    // Use array...
}
finally
{
    array.Dispose();
}
```

### DynamicBuffer

`DynamicBuffer<T>` provides variable-length arrays as ECS components, perfect for collections that change size.

**Key Features:**
- Component data that can grow/shrink
- Optimized for small arrays (internal capacity)
- Automatic memory management
- Burst-compatible operations

**Component Definition:**
```csharp
using Unity.Entities;

[InternalBufferCapacity(8)] // Optimize for 8 elements
public struct MyBufferElement : IBufferElementData
{
    public float3 position;
    public float health;
    
    // Implicit conversion for convenience
    public static implicit operator float3(MyBufferElement element) => element.position;
    public static implicit operator MyBufferElement(float3 position) => new() { position = position };
}
```

**Basic Operations:**
```csharp
public partial struct BufferSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var buffer in SystemAPI.Query<DynamicBuffer<MyBufferElement>>())
        {
            // Add elements
            buffer.Add(new float3(1, 2, 3));
            buffer.Add(new MyBufferElement { position = new float3(4, 5, 6), health = 100f });
            
            // Access elements
            if (buffer.Length > 0)
            {
                var first = buffer[0];
                buffer[0] = new float3(10, 20, 30); // Modify
            }
            
            // Remove elements
            if (buffer.Length > 5)
            {
                buffer.RemoveAt(0); // Remove first
                buffer.RemoveRange(0, 2); // Remove range
            }
            
            // Clear all
            buffer.Clear();
            
            // Iterate
            for (int i = 0; i < buffer.Length; i++)
            {
                float3 pos = buffer[i].position;
                // Process position...
            }
        }
    }
}
```

**Advanced Buffer Operations:**
```csharp
public partial struct AdvancedBufferSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (buffer, entity) in 
                 SystemAPI.Query<DynamicBuffer<MyBufferElement>>().WithEntityAccess())
        {
            // Resize buffer
            buffer.Capacity = 100; // Set minimum capacity
            buffer.EnsureCapacity(50); // Ensure at least 50 elements
            
            // Convert to NativeArray for jobs
            var nativeArray = buffer.AsNativeArray();
            
            // Reinterpret as different type (unsafe)
            var floatBuffer = buffer.Reinterpret<float>();
            
            // Copy from/to other collections
            var sourceArray = new NativeArray<MyBufferElement>(10, Allocator.Temp);
            buffer.CopyFrom(sourceArray);
            
            sourceArray.Dispose();
        }
    }
}
```

**Buffer with Jobs:**
```csharp
[BurstCompile]
public partial struct ProcessBufferJob : IJobEntity
{
    public float deltaTime;
    
    void Execute(DynamicBuffer<MyBufferElement> buffer)
    {
        // Process each element in the buffer
        for (int i = 0; i < buffer.Length; i++)
        {
            var element = buffer[i];
            element.position.y += deltaTime;
            buffer[i] = element; // Write back
        }
        
        // Add new element based on some condition
        if (buffer.Length < 10)
        {
            buffer.Add(new MyBufferElement 
            { 
                position = new float3(UnityEngine.Random.value, 0, 0),
                health = 100f 
            });
        }
    }
}
```

**Performance Considerations:**
```csharp
// Good: Set internal buffer capacity based on typical usage
[InternalBufferCapacity(16)] // Most entities have ~16 elements
public struct OptimizedBuffer : IBufferElementData
{
    public int value;
}

// Batch operations when possible
foreach (var buffer in SystemAPI.Query<DynamicBuffer<MyBufferElement>>())
{
    if (buffer.Length > 100)
    {
        // Use NativeArray for bulk operations
        var array = buffer.AsNativeArray();
        // Process array efficiently...
    }
}
```

## MonoBehaviour Integration

### Interacting between MonoBehaviour and ECS

```csharp
// In MonoBehaviour
void Start()
{
    World.DefaultGameObjectInjectionWorld
         .GetExistingSystem<PlayerInputSystem>()
         .OnShoot += HandleShoot;
}

void HandleShoot(object sender, EventArgs e)
{
    // Handle shoot event
}

public partial struct PlayerInputSystem : ISystem
{
    public event Action OnShoot;

    public void OnUpdate(ref SystemState state)
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            OnShoot?.Invoke();
        }
    }
}
```

