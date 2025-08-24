# Unity ECS (Entity Component System)

Unity ECS is a data-oriented design pattern that provides high performance and enables massive parallelization through the Burst compiler and Job System.

## Table of Contents

1. [Resources](#resources)
2. [Setup and Configuration](#setup-and-configuration)
3. [Core Concepts](#core-concepts)
4. [Components](#components)
5. [Entities](#entities) 
6. [Systems](#systems)
7. [Queries and Filtering](#queries-and-filtering)
8. [Aspects](#aspects)
9. [Entity Management](#entity-management)
10. [Prefabs and Spawning](#prefabs-and-spawning)
11. [World Management](#world-management)
12. [Performance Optimization](#performance-optimization)
13. [Advanced Features](#advanced-features)
14. [Best Practices](#best-practices)
15. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
16. [Quick Reference](#quick-reference)

## Resources

- [Code Monkey ECS RTS game](https://www.youtube.com/watch?v=1gSnTlUjs-s)
- [Code Monkey 1h ECS Extreme Performance](https://www.youtube.com/watch?v=4ZYn9sR3btg)
- [Unity ECS Documentation](https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/index.html)

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
   - Unity Physics (optional)

3. **Create Entity Subscene**
   `Create` > `New subscene` > `Empty scene`

### Entities Hierarchy Window

Access via: `Window` > `Entities` > `Hierarchy`
![[Pasted image 20250812103741.png]]

## Entities Inspector Authoring vs Runtime

![[Pasted image 20250821191626.png]]
## Scene view Authoring Data vs Runtime Data

![[Pasted image 20250821192640.png]]
## Core Concepts

Unity ECS follows the Entity-Component-System pattern:

- **Entity**: A unique identifier (like GameObject but lightweight)
- **Component**: Pure data containers (no behavior)
- **System**: Logic that processes entities with specific components

### Data-Oriented Design Benefits

- **Performance**: Cache-friendly memory layout
- **Parallelization**: Easy to process entities in parallel
- **Scalability**: Handle thousands of entities efficiently
- **Predictability**: No inheritance hierarchies or virtual calls

### Archetype concept 

An **Archetype** is a unique combination of components that defines the structure of an entity. Entities with the same archetype share the same memory layout, allowing for efficient processing.

 For example, in the following diagram, all the entities in a world that have the components `Speed`, `Direction`, `Position`, and `Renderer` and no others share the archetype labelled **X**. All the entities that have component types `Speed`, `Direction`, and `Position` and no others share a different archetype labelled **Y**.

[Archetype concept in documentation](https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/concepts-archetypes.html)


![[Pasted image 20250822131906.png]]

> ❗️**IMPORTANT:** 
>Moving entities frequently is resource-intensive and reduces the performance of your application. For more information, refer to the documentation on **Structural change concepts**.

### Structural Changes

Structureal changes modify the archetype of an entity by adding or removing components. These operations are costly because they may involve memory allocation and data copying.

❗️Structural changes include:

- Adding or removing components
- Creating or destroying entities
- Setting a shared component value



## Components

### IComponentData

`IComponentData` defines data components that store information for entities. These are pure data structures without behavior.

```csharp
using Unity.Entities;

public struct RotationSpeed : IComponentData
{
    public float Value; 
}

public struct Health : IComponentData
{
    public float Current;
    public float Maximum;
}

public struct Velocity : IComponentData
{
    public float3 Value;
}
```

### List of built-in components

- `LocalTranform` - position, rotation, scale
    - `Translation` - position only
    - `Rotation` - rotation only
    - `NonUniformScale` - scale only
- `Parent` - parent entity reference
- `Child` - child entity reference

- `RenderMesh` - mesh and material for rendering

- `PhysicsVelocity` - velocity and angular velocity
- `PhysicsCollider` - collider shape

### Managed vs Unmanaged Components 

**Managed** vs **Unmanaged** components:
`class` vs `struct`:

❗️ **Unmanaged** over **Managed** for performance and `Burst` compatibility and `Jobs`.

#### Managed Component(class)

- You can't access them in `Burst` compiled code
- You can't use them in `jobs`
- They can hold references to managed objects (like `string`, `List<T>`, etc

- [documenation on Managed](https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/components-managed.html)


```csharp

public class ManagedComponent : IComponentData
{
    public string Name; // Managed type, not Burst-compatible
}
```

#### Unmanaged Components(struct)

- [documentation on Unmanaged](https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/components-unmanaged.html)

**Can use with types:**
- **Bittble** types (`int`, `float`, `bool`,`char`)
- Fixed-size structs (`float3`, `quaternion`)
- `BlobAssetReference<T>` - for large read-only data
- `Collections.NativeArray<T>`, `NativeList<T>`, `NativeHashMap<TKey, TValue>`, etc.
- `Collections.FixedString32Bytes`, `FixedString64Bytes`, etc.
- `collections.DynamicBuffer<T>`


```csharp
public struct UnmanagedComponent : IComponentData
{
    public int Value; // Unmanaged type, Burst-compatible
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

### Tag Components  

Tag components are `IComponentData` without data, used purely for identification and filtering.

```csharp
public struct PlayerTag : IComponentData { }
public struct EnemyTag : IComponentData { }
public struct DeadTag : IComponentData { }
public struct SelectedTag : IComponentData { }
```

### IEnableableComponent

`IEnableableComponent` allows you to enable or disable components without structural changes (no entity recreation).
> ❗️ Entities with disabled components are excluded from queries by default.

**Query Method to select enabled components:**

`.WithPreesent<T>()` - to select entities with component T (enabled or disabled)
`.WithEnnbled<T>()` - only enabled components
`.WithDisabled<T>()` - only disabled components

```csharp
public struct AIEnabled : IComponentData, IEnableableComponent { }

// Usage in system
public partial struct AISystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (entity, aiState) in SystemAPI.Query<Entity, RefRO<AIState>>().WithAll<AIEnabled>())
        {
            // Conditionally disable AI
            if (aiState.ValueRO.ShouldStop)
                SystemAPI.SetComponentEnabled<AIEnabled>(entity, false);
        }
    }
}
```

### ISharedComponentData

Shared components group entities with the same data values together, enabling efficient batch processing.

```csharp
public struct RenderMesh : ISharedComponentData
{
    public Mesh Mesh;
    public Material Material;
}

public struct TeamData : ISharedComponentData
{
    public int TeamID;
    public Color TeamColor;
}
```

**Usage:**
```csharp
// Entities with the same shared component values are grouped together
SystemAPI.EntityManager.SetSharedComponent(entity, new TeamData 
{ 
    TeamID = 1, 
    TeamColor = Color.red 
});
```

### ISystemStateComponent

System state components persist when regular components are removed, enabling proper cleanup.

```csharp
public struct AudioSourceSystemState : ISystemStateComponent
{
    public Entity AudioEntity;
}

public partial struct AudioCleanupSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // Clean up when AudioSource component is removed, but the state remains
        foreach (var (stateComponent, entity) in 
                 SystemAPI.Query<RefRO<AudioSourceSystemState>>()
                          .WithNone<AudioSource>()
                          .WithEntityAccess())
        {
            // Clean up audio resources
            SystemAPI.EntityManager.DestroyEntity(stateComponent.ValueRO.AudioEntity);
            SystemAPI.EntityManager.RemoveComponent<AudioSourceSystemState>(entity);
        }
    }
}
```

## Entities

`Entity` is a struct that represents an entity in Unity ECS. Contains ID and version for identification.

> **Think of it like `GameObject` in Unity, but without any components.**

### Creating Entities

```csharp
// Create empty entity
Entity entity = SystemAPI.EntityManager.CreateEntity();

// Create with archetype
EntityArchetype archetype = SystemAPI.EntityManager.CreateArchetype(
    typeof(LocalTransform),
    typeof(RotationSpeed)
);
Entity entity = SystemAPI.EntityManager.CreateEntity(archetype);

// Add components
SystemAPI.EntityManager.AddComponentData(entity, new RotationSpeed { Value = 1.0f });
```

### TransformUsageFlags

`TransformUsageFlags` defines how the transform of an entity will be used:

- **Dynamic**: For entities that move or rotate frequently
- **None**: Entity will not have a transform
- **WorldSpace**: Entity position is set in world coordinates

```csharp
// In Baker
Entity entity = GetEntity(TransformUsageFlags.Dynamic);
Entity staticEntity = GetEntity(TransformUsageFlags.None);
Entity worldEntity = GetEntity(TransformUsageFlags.WorldSpace);
```

### Singleton Entities

A singleton entity has only one instance in the world, used for global data.

```csharp
public struct SpawnCubesConfig : IComponentData
{
    public int Count;
    public float SpawnRate;
}

public partial struct SpawnCubesSystem : ISystem
{
    public void OnCreate(ref SystemState state)
    {
        state.RequireForUpdate<SpawnCubesConfig>();
    }
    
    public void OnUpdate(ref SystemState state)
    {
        var config = SystemAPI.GetSingleton<SpawnCubesConfig>();
        
        // Modify singleton data
        config.Count++;
        SystemAPI.SetSingleton(config);
    }
}
```

### Entity static class 

```csharp 
Entity entity = Entity.Null; // Represents no entity
```

### EntityManager 

`EntityManager` is the main API for creating, destroying, and managing entities and their components.

```csharp

EntityManger entityManager = World.DefaultGameObjectInjectionWorld.EntityManager
Entity entity = entityManager.CreateEntity();

EntityQuery query = new EntityQueryBuilder(Allocator.Temp)
                        .WithAll<LocalTransform, RotationSpeed>()
                        .Build(entityManager);
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

### ISystem Structure and Lifecycle

```csharp
public partial struct RotationSystem : ISystem
{
    public void OnCreate(ref SystemState state) 
    {
        // Initialize system (called once)
        // Set up requirements, queries, etc.
    } 
    
    public void OnUpdate(ref SystemState state) 
    {
        // Process entities every frame
        // Main system logic goes here
    }
    
    public void OnDestroy(ref SystemState state) 
    {
        // Clean up resources (called once)
        // Dispose unmanaged resources
    } 
}
```

### System Requirements

```csharp
public partial struct MovementSystem : ISystem
{
    public void OnCreate(ref SystemState state)
    {
        // System only runs when entities with these components exist
        state.RequireForUpdate<RotationSpeed>();
        state.RequireForUpdate<PlayerInput>();
    }
}
```

### System Examples

**Simple Rotation System:**
```csharp
using Unity.Entities;
using Unity.Transforms;
using Unity.Mathematics;

public partial struct RotationSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (localTransform, rotationSpeed) 
                 in SystemAPI.Query<RefRW<LocalTransform>, RefRO<RotationSpeed>>()) 
        {
            localTransform.ValueRW = localTransform.ValueRO.RotateY(
                rotationSpeed.ValueRO.Value * deltaTime
            ); 
        }
    } 
}
```

**Movement System with Multiple Components:**
```csharp
public partial struct MovementSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (transform, velocity, speed) in 
                 SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>, RefRO<MovementSpeed>>()
                          .WithNone<DeadTag>()) // Exclude dead entities
        {
            float3 movement = velocity.ValueRO.Value * speed.ValueRO.Value * deltaTime;
            transform.ValueRW.Position += movement;
        }
    }
}
```

**Disabling a System:**
```csharp
public void OnUpdate(ref SystemState state)
{
    if (someCondition)
    {
        state.Enabled = false;
        return;
    }
    // Rest of system logic...
}
```

## Queries and Filtering

### SystemAPI.Query Basics

SystemAPI.Query provides type-safe, Burst-friendly entity iteration:

```csharp
// Basic query
foreach (var (transform, velocity) in 
         SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>())
{
    // Process entities
}
```


### Reference Wrappers

| Wrapper | Access | Usage |
|---------|--------|---------|
| `RefRO<T>` | Read-only | `RefRO<RotationSpeed>` |
| `RefRW<T>` | Read-write | `RefRW<LocalTransform>` |
| `EnabledRefRO<T>` | Read-only enabled components | For IEnableableComponent |
| `EnabledRefRW<T>` | Read-write enabled components | For IEnableableComponent |

### Query Filtering

**Include entities with specific components:**
```csharp
SystemAPI.Query<RefRO<Health>>()
         .WithAll<PlayerTag, AliveTag>();
```

**Include entities with at least one component:**
```csharp
SystemAPI.Query<RefRO<Health>>()
         .WithAny<ZombieTag, VampireTag>();
```

**Exclude entities with specific components:**
```csharp
SystemAPI.Query<RefRO<Health>>()
         .WithNone<DeadTag, DisabledTag>();
```

**Access entity in query:**
```csharp
foreach ((var transform, var entity) in 
         SystemAPI.Query<RefRO<LocalTransform>>()
                  .WithAll<PlayerTag>()
                  .WithEntityAccess())
{
    // Use entity for additional operations
}
```

**Include disabled components:**
```csharp
SystemAPI.Query<RefRW<AIState>>()
         .WithDisabled<AIEnabled>();
```

### EntityQueryBuilder (Advanced)

`EntityQuery` - is a more advanced way to define queries, useful for complex filtering and caching. 

For complex queries that need to be cached or reused:

```csharp
public partial struct ComplexQuerySystem : ISystem
{
    private EntityQuery playerQuery;
    
    public void OnCreate(ref SystemState state)
    {
        playerQuery = SystemAPI.QueryBuilder()
            .WithAll<LocalTransform, Health>()
            .WithAny<PlayerTag, NPCTag>()
            .WithNone<DeadTag>()
            .Build();
    }
    
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (transform, health) in 
                 SystemAPI.Query<RefRW<LocalTransform>, RefRW<Health>>()
                          .WithEntityQueryOptions(EntityQueryOptions.IncludeDisabledEntities))
        {
            // Process entities
        }
    }
}
```

### Component Lookups

For random access to component data outside of queries:

```csharp
public partial struct LookupSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var transformLookup = SystemAPI.GetComponentLookup<LocalTransform>(isReadOnly: false);
        var healthLookup = SystemAPI.GetComponentLookup<Health>(isReadOnly: true);
        
        foreach (var (targetRef, entity) in 
                 SystemAPI.Query<RefRO<Target>>().WithEntityAccess())
        {
            Entity targetEntity = targetRef.ValueRO.Entity;
            
            // Check if target has component before accessing
            if (healthLookup.HasComponent(targetEntity))
            {
                Health targetHealth = healthLookup[targetEntity];
                
                if (targetHealth.Current <= 0 && transformLookup.HasComponent(targetEntity))
                {
                    var targetTransform = transformLookup[targetEntity];
                    targetTransform.Position = new float3(0, -100, 0); // Move underground
                    transformLookup[targetEntity] = targetTransform;
                }
            }
        }
    }
}
```

### Singletons and Special Cases

**Getting a Single Component:**
```csharp
var playerHealth = SystemAPI.GetSingleton<Health>();

var ecb = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                   .CreateCommandBuffer(World.Unmanaged);
```

**Performance Tips:**
- Use `RefRO` unless you need to modify — this allows Burst optimizations
- Chain filters to reduce the number of entities processed
- Use `.WithEntityAccess()` only if you really need the entity ID

## Aspects

`IAspect` groups related component data into a cohesive interface, improving code organization and reusability.

### Aspect Definition

```csharp
using Unity.Entities;
using Unity.Transforms;
using Unity.Mathematics;

public readonly partial struct MovementAspect : IAspect
{
    readonly RefRW<LocalTransform> transform;
    readonly RefRO<Velocity> velocity;
    readonly RefRO<MovementSpeed> speed;
    
    // Properties for clean access
    public float3 Position 
    { 
        get => transform.ValueRO.Position;
        set => transform.ValueRW.Position = value;
    }
    
    public float3 Forward => transform.ValueRO.Forward();
    
    // Methods encapsulate behavior
    public void Move(float deltaTime)
    {
        Position += velocity.ValueRO.Value * speed.ValueRO.Value * deltaTime;
    }
    
    public void RotateTowards(float3 direction, float deltaTime)
    {
        var targetRotation = quaternion.LookRotationSafe(direction, math.up());
        transform.ValueRW.Rotation = math.slerp(
            transform.ValueRO.Rotation, 
            targetRotation, 
            deltaTime * 5.0f
        );
    }
}
```

### Using Aspects

**Before (verbose query):**
```csharp
foreach (var (localTransform, velocity, speed) in 
         SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>, RefRO<MovementSpeed>>()
                  .WithAll<PlayerTag>())
{
    float3 movement = velocity.ValueRO.Value * speed.ValueRO.Value * SystemAPI.Time.DeltaTime;
    localTransform.ValueRW.Position += movement;
}
```

**After (clean aspect):**
```csharp
foreach (var movementAspect in SystemAPI.Query<MovementAspect>().WithAll<PlayerTag>())
{
    movementAspect.Move(SystemAPI.Time.DeltaTime);
}
```

## Entity Management

### EntityCommandBuffer (ECB)

**EntityCommandBuffer (ECB)** records structural changes to entities and applies them later, enabling safe modifications from jobs or during iteration.

```csharp
public partial struct SpawnSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var ecb = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                           .CreateCommandBuffer(state.WorldUnmanaged);
        
        var spawner = SystemAPI.GetSingleton<SpawnerConfig>();
        
        for (int i = 0; i < spawner.Count; i++)
        {
            Entity newEntity = ecb.Instantiate(spawner.Prefab);
            ecb.SetComponent(newEntity, new LocalTransform 
            { 
                Position = new float3(i, 0, 0), 
                Rotation = quaternion.identity,
                Scale = 1.0f
            });
            ecb.AddComponent(newEntity, new Velocity { Value = new float3(0, 1, 0) });
        }
    }
}
```

### ECB System Groups

Different ECB systems for different timing:

- `BeginInitializationEntityCommandBufferSystem`: Start of frame
- `EndInitializationEntityCommandBufferSystem`: After initialization
- `BeginSimulationEntityCommandBufferSystem`: Start of simulation
- `EndSimulationEntityCommandBufferSystem`: End of simulation
- `BeginPresentationEntityCommandBufferSystem`: Start of presentation

### Entity Destruction with Cleanup

```csharp
public partial struct DestroySystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var ecb = SystemAPI.GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()
                           .CreateCommandBuffer(state.WorldUnmanaged);
        
        foreach (var (health, entity) in 
                 SystemAPI.Query<RefRO<Health>>().WithEntityAccess())
        {
            if (health.ValueRO.Current <= 0)
            {
                // Add cleanup component first
                ecb.AddComponent<DestroyedTag>(entity);
                
                // Then schedule destruction
                ecb.DestroyEntity(entity);
            }
        }
    }
}
```

## Prefabs and Spawning

### Entity Prefabs

Entity prefabs are baked versions of GameObjects that can be instantiated efficiently:

```csharp
public struct SpawnerConfig : IComponentData
{
    public Entity Prefab;
    public int Count;
    public float SpawnRate;
    public float3 SpawnArea;
}

public class SpawnerAuthoring : MonoBehaviour
{
    public GameObject prefab;
    public int count = 100;
    public float spawnRate = 10.0f;
    public Vector3 spawnArea = new Vector3(10, 0, 10);
    
    class Baker : Baker<SpawnerAuthoring>
    {
        public override void Bake(SpawnerAuthoring authoring)
        {
            Entity entity = GetEntity(TransformUsageFlags.None);
            AddComponent(entity, new SpawnerConfig
            {
                Prefab = GetEntity(authoring.prefab, TransformUsageFlags.Dynamic),
                Count = authoring.count,
                SpawnRate = authoring.spawnRate,
                SpawnArea = authoring.spawnArea
            });
        }
    }
}
```

### Instantiation Patterns

**Basic Instantiation:**
```csharp
Entity newEntity = SystemAPI.EntityManager.Instantiate(prefabEntity);
```

**Batch Instantiation:**
```csharp
using Unity.Collections;

var entities = new NativeArray<Entity>(100, Allocator.Temp);
SystemAPI.EntityManager.Instantiate(prefabEntity, entities);

// Modify each instance
for (int i = 0; i < entities.Length; i++)
{
    SystemAPI.EntityManager.SetComponentData(entities[i], new LocalTransform
    {
        Position = new float3(i, 0, 0),
        Rotation = quaternion.identity,
        Scale = 1.0f
    });
}

entities.Dispose();
```

**ECB Spawning:**
```csharp
public partial struct WaveSpawnerSystem : ISystem
{
    private float nextSpawnTime;
    
    public void OnUpdate(ref SystemState state)
    {
        if (SystemAPI.Time.ElapsedTime < nextSpawnTime) return;
        
        var ecb = SystemAPI.GetSingleton<BeginSimulationEntityCommandBufferSystem.Singleton>()
                           .CreateCommandBuffer(state.WorldUnmanaged);
        
        var config = SystemAPI.GetSingleton<SpawnerConfig>();
        
        for (int i = 0; i < config.Count; i++)
        {
            Entity enemy = ecb.Instantiate(config.Prefab);
            
            float3 spawnPosition = new float3(
                UnityEngine.Random.Range(-config.SpawnArea.x, config.SpawnArea.x),
                0,
                UnityEngine.Random.Range(-config.SpawnArea.z, config.SpawnArea.z)
            );
            
            ecb.SetComponent(enemy, LocalTransform.FromPosition(spawnPosition));
            ecb.AddComponent(enemy, new Velocity { Value = new float3(0, 0, 1) });
        }
        
        nextSpawnTime = (float)SystemAPI.Time.ElapsedTime + (1.0f / config.SpawnRate);
    }
}
```

## World Management

### Multiple Worlds

Unity ECS supports multiple worlds for different purposes:

```csharp
// Create new world
World customWorld = new World("CustomWorld");

// Get default world
World defaultWorld = World.DefaultGameObjectInjectionWorld;

// Switch between worlds
World.DefaultGameObjectInjectionWorld = customWorld;

// Clean up
customWorld.Dispose();
```

### World Types

- **Default World**: Main game world with standard systems
- **Custom Worlds**: Specialized worlds (e.g., UI, background simulation)
- **Client/Server Worlds**: For netcode applications

### MonoBehaviour Integration

```csharp
// Interacting between MonoBehaviour and ECS
public class GameManager : MonoBehaviour
{
    void Start()
    {
        // Get system from default world
        var playerSystem = World.DefaultGameObjectInjectionWorld
                               .GetExistingSystemManaged<PlayerInputSystem>();
        
        if (playerSystem != null)
        {
            // Configure system
            playerSystem.Enabled = true;
        }
    }
    
    void Update()
    {
        // Access singleton data
        if (World.DefaultGameObjectInjectionWorld.EntityManager
                 .HasSingleton<GameState>())
        {
            var gameState = World.DefaultGameObjectInjectionWorld.EntityManager
                                 .GetSingleton<GameState>();
            // Use game state...
        }
    }
}
```

## Performance Optimization

### Burst Compilation

Burst compilation provides massive performance improvements by compiling to highly optimized native code.

```csharp
[BurstCompile]
public partial struct HighPerformanceSystem : ISystem
{
    [BurstCompile]
    public void OnUpdate(ref SystemState state) 
    {
        foreach (var (transform, velocity) in 
                 SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>())
        {
            transform.ValueRW.Position += velocity.ValueRO.Value * SystemAPI.Time.DeltaTime;
        }
    }
}
```

### Job System 

- [Writing multithreaded code with the Job System](https://docs.unity3d.com/Manual/job-system.html)

**ref/in** access modifiers in jobs:

- `ref`-  like `RefRW<>` meaning access **read/write** . 
- `in` -  like `RefRO<>` meaning access read-only.


#### Job Interfaces
- `IJob` - Basic job interface for single-threaded jobs ❌**ECS**
- `IJobParallelFor` - Parallel job interface for processing arrays ❌**ECS**
- `IJobEntity` - Job interface for processing *entities* with components ✅**ECS**
- `IJobChunk` - Job interface for processing *chunks* of entities ✅**ECS**

#### Job Scheduling

- `job.Run()` - Schedules a job to run immediately (single-threaded) 
- `job.Schedule()` - Schedules a job to run on the next frame (multi-threaded)
- `job.ScheduleParallel()` - Schedules a job to run in parallel across multiple threads (multi-threaded)
- `job.ScheduleBatchedJobs()` - Schedules all pending jobs to run immediately (useful for testing)


#### IJobEntity Example

```csharp
[BurstCompile]
public partial struct MovementJob : IJobEntity
{
    public float deltaTime;
    
    public void Execute(ref LocalTransform transform, in Velocity velocity)
    {
        transform.Position += velocity.Value * deltaTime;
    }
}

public partial struct MovementSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var job = new MovementJob
        {
            deltaTime = SystemAPI.Time.DeltaTime
        };
        
        state.Dependency = job.ScheduleParallel(state.Dependency);
    }
}
```

### Memory Management

### Allocators 

- [Documenation link](https://docs.unity3d.com/Packages/com.unity.entities@1.0/manual/allocators-overview.html)

Alloocators define the lifetime and preformance characteristics of native collections.

- `Allocator.Temp` - Temporary memory, valid for one frame
- `Allocator.TempJob` - Temporary memory, valid for the duration of a job
- `Allocator.Persistent` - Long-term memory, must be manually disposed 
> ❗️** Avoid using** `Allocator.Persistent` unless necessary to prevent memory leaks. Because it's stays lifetime and is slowest of **Allocators**
- `Allocator.None` - No allocation, used for stack-allocated data

#### Allocators usecases 

```csharp
new NativeArray<int>(100, Allocator.Temp); // Valid for one frame
EntityQuerBuilder(Allocator.TempJob) // Valid for job duration
EntityQuery query = new EntityQueryBuilder(Allocator.Persistent) // Valid until manually disposed
EntityManger.CreateArchetype(typeof(ComponentA), typeof(ComponentB), Allocator.Persistent); // Valid until manually disposed

```

### Native Collections 

- `NativeArray<T>` - Fixed-size array
    - `NativeList<T>` - Dynamic-size list
    - `NativeHashMap<TKey, TValue>` - Key-value pairs
    - `NativeQueue<T>` - FIFO queue
    - `NativeStack<T>` - LIFO stack
- `DynamicBuffer<T>` - Variable-length array attached to entities
- `BlobAssetReference<T>` - Immutable, read-only data
- `EntityQuery` - Is not a collction but used Allocator to define lifetime


**NativeArray for temporary data:**
```csharp
using Unity.Collections;

public partial struct DataProcessingSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        using var positions = new NativeArray<float3>(100, Allocator.TempJob);
        
        // Process data...
    } // Automatic disposal
}
```

**DynamicBuffer for variable-length data:**
```csharp
[InternalBufferCapacity(8)]
public struct PathPoint : IBufferElementData
{
    public float3 Position;
}

public partial struct PathfindingSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var pathBuffer in SystemAPI.Query<DynamicBuffer<PathPoint>>())
        {
            // Add waypoint
            pathBuffer.Add(new PathPoint { Position = new float3(1, 0, 1) });
            
            // Process path
            for (int i = 0; i < pathBuffer.Length; i++)
            {
                float3 waypoint = pathBuffer[i].Position;
                // Navigate to waypoint...
            }
        }
    }
}
```

## Advanced Features

### Mathematics Package

Unity Mathematics provides Burst-compatible math types:

```csharp
using Unity.Mathematics;

// Vector types
float2 uv = new float2(0.5f, 0.5f);
float3 position = new float3(1, 2, 3);
float4 color = new float4(1, 0, 0, 1);

// Quaternion operations
quaternion rotation = quaternion.EulerXYZ(0, math.radians(90), 0);
quaternion rotY = quaternion.RotateY(math.radians(45));
quaternion combined = math.mul(rotation, rotY);
transform.Rotation = quaternion.LookRotation(forward, math.up())

// Common operations
float length = math.length(position);
float3 normalized = math.normalize(position);
float distance = math.distance(float3.zero, position);
float dotProduct = math.dot(new float3(1, 0, 0), new float3(0, 1, 0));
float3 crossProduct = math.cross(new float3(1, 0, 0), new float3(0, 1, 0));

// Interpolation
float3 lerped = math.lerp(position, float3.zero, 0.5f);
```

**Key Math Functions:**

- `math.up()` - float3(0,1,0)
- `math.mul()` - Multiply quaternions or matrices
- `math.lerp()` - Linear interpolation between values
- `math.slerp()` - Spherical linear interpolation for `quaternion`'s
- `math.dot()` - Dot product (alignment measure)
- `math.cross()` - Cross product (perpendicular vector)
- `math.radians()` - Convert degrees to radians
- `math.degrees()` - Convert radians to degrees
- `math.normalize()` - Normalize vector to unit length
- `math.length()` - Get vector magnitude

### System Groups and Ordering

```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateBefore(typeof(MovementSystem))]
public partial struct InputSystem : ISystem
{
    // This system runs before MovementSystem
}

[UpdateInGroup(typeof(SimulationSystemGroup), OrderFirst = true)]
public partial struct EarlySystem : ISystem
{
    // This system runs first in the group
}

[UpdateInGroup(typeof(SimulationSystemGroup), OrderLast = true)]
public partial struct LateSystem : ISystem
{
    // This system runs last in the group
}
```

### Custom System Groups

```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
public class AISystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(AISystemGroup))]
public partial struct AIMovementSystem : ISystem { }

[UpdateInGroup(typeof(AISystemGroup))]
public partial struct AIDecisionSystem : ISystem { }
```

## Best Practices

### Component Design

✅ **Good - Pure data:**
```csharp
public struct PlayerData : IComponentData
{
    public float MovementSpeed;
    public int Health;
    public int MaxHealth;
}
```

❌ **Bad - References to managed objects:**
```csharp
public struct BadComponent : IComponentData
{
    public Transform transform; // Don't store Unity object references
    public List<int> items;     // Don't use managed collections
}
```

### System Design

✅ **Good - Single responsibility:**
```csharp
public partial struct MovementSystem : ISystem
{
    // Only handles movement logic
}

public partial struct HealthSystem : ISystem
{ 
    // Only handles health logic
}
```

❌ **Bad - Multiple responsibilities:**
```csharp
public partial struct EverythingSystem : ISystem
{
    // Handles movement, health, AI, rendering, etc.
}
```

### Performance Guidelines

1. **Use `ISystem` over `SystemBase`** for better performance
2. **Minimize entity structural changes** during gameplay
3. **Use `EntityCommandBuffer`** for deferred structural changes
4. **Batch operations** when possible
5. **Use appropriate `Allocator`** types for temporary data
6. **Profile and measure** performance improvements

### Memory Management

```csharp
// Good - Automatic disposal
using var tempArray = new NativeArray<float>(100, Allocator.TempJob);

// Good - Explicit disposal
var persistentArray = new NativeArray<float>(100, Allocator.Persistent);
// ... use array ...
persistentArray.Dispose();

// Bad - Memory leak
var leakyArray = new NativeArray<float>(100, Allocator.Persistent);
// Missing Dispose() call
```

## Debugging and Troubleshooting

### Entity Debugger

Access via: `Window` > `Entities` > `Systems` or `Hierarchy`

**Common debugging tasks:**
- View entity composition and component values
- Monitor system execution order and timing
- Track entity creation/destruction
- Inspect chunk utilization

### Common Issues and Solutions

**Issue: System not running**
```csharp
// Solution: Check system requirements
public void OnCreate(ref SystemState state)
{
    state.RequireForUpdate<RequiredComponent>();
}
```

**Issue: Structural changes during iteration**
```csharp
// Problem:
foreach (var entity in SystemAPI.Query<Entity>())
{
    SystemAPI.EntityManager.AddComponent<NewComponent>(entity); // ❌ Dangerous
}

// Solution: Use ECB
var ecb = SystemAPI.GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()
                   .CreateCommandBuffer(state.WorldUnmanaged);

foreach (var entity in SystemAPI.Query<Entity>())
{
    ecb.AddComponent<NewComponent>(entity); // ✅ Safe
}
```

**Issue: Performance problems**
- Use Burst Profiler to identify bottlenecks
- Check for unnecessary boxing/managed allocations
- Verify systems are using `ISystem` and `[BurstCompile]`
- Monitor chunk utilization in Entity Debugger

### Profiling Tips

1. **Use Unity Profiler** with ECS-specific markers
2. **Enable Burst Inspector** for job analysis
3. **Monitor memory allocation** in Memory Profiler
4. **Check entity chunk fragmentation** in Entity Debugger

### Error Messages Guide

**"SystemState.RequireForUpdate" not met:**
- Ensure required components exist in the world
- Check if entities with required components are being created

**"NativeArray has not been disposed":**
- Always dispose NativeArrays and other native containers
- Use `using` statements for automatic disposal

**"InvalidOperationException during iteration":**
- Don't perform structural changes during entity iteration
- Use EntityCommandBuffer for deferred operations

## Quick Reference

### Key Types
- `Entity` - Unique identifier
- `IComponentData` - Pure data component
- `ISystem` - High-performance system
- `SystemAPI` - Main API for queries and singletons
- `EntityCommandBuffer` - Deferred structural changes

### Common Patterns
```csharp
// Query with filtering
foreach (var (transform, health) in 
         SystemAPI.Query<RefRW<LocalTransform>, RefRO<Health>>()
                  .WithAll<PlayerTag>()
                  .WithNone<DeadTag>())

// Singleton access
var config = SystemAPI.GetSingleton<GameConfig>();
SystemAPI.SetSingleton(newConfig);

// ECB usage
var ecb = SystemAPI.GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()
                   .CreateCommandBuffer(state.WorldUnmanaged);

// Component lookup
var healthLookup = SystemAPI.GetComponentLookup<Health>(isReadOnly: true);
```

This comprehensive guide covers Unity ECS from basic concepts to advanced patterns. Use it as a reference while developing your ECS-based games and applications.
