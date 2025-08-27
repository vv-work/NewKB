# Unity ECS Physics 🎯

Unity's Entity Component System (ECS) physics provides high-performance physics simulation using the Unity Physics package. This system is built from the ground up to work seamlessly with DOTS (Data-Oriented Technology Stack).

## Core Concepts

### Physics World
The physics world is the container for all physics objects and handles simulation updates.

```csharp
using Unity.Physics;
using Unity.Physics.Systems;

public partial class CustomPhysicsSystem : SystemBase
{
    protected override void OnUpdate()
    {
        var physicsWorld = SystemAPI.GetSingleton<PhysicsWorldSingleton>().PhysicsWorld;
        
        // Access physics world data
        var bodies = physicsWorld.Bodies;
        var staticBodies = physicsWorld.StaticBodies;
        var dynamicBodies = physicsWorld.DynamicBodies;
    }
}
```

### Physics world  and Collision World Raycastin example in  MonoBehaviour

```csharp

EntityManager entityManager =  World.DefaultGameObjectInjectionWorld.EntityManager;
entityQuery =  entityManager.CreateEntityQuery(typeof(PhysicsWorldSingleton));
//todo: Note taking singleton 
var physicsWorldSingleton = entityQuery.GetSingleton<PhysicsWorldSingleton>();
var collisionWorld = physicsWorldSingleton.CollisionWorld; 

var cameraRay = Camera.main.ScreenPointToRay(mousePosition);

int unitLayer = 7;
RaycastInput raycastInput = new RaycastInput()
{
    //todo:note Geting point
    Start = cameraRay.GetPoint(0f),
    End = cameraRay.GetPoint(1000f), 

    Filter = new CollisionFilter()
    {
        BelongsTo = ~0u,
        CollidesWith = GameAssets.UNITY_LAYER,
        GroupIndex = 0,
    }

};

if (collisionWorld.CastRay(raycastInput, out Unity.Physics.RaycastHit hit)) {
    //todo: note .HasComponent<T>
    if (entityManager.HasComponent<Unit>(hit.Entity))
    { 
        entityManager.SetComponentEnabled<Selected>(hit.Entity,true);
        Selected selected = entityManager.GetComponentData<Selected>(hit.Entity);
        selected.OnSelected = true;
        entityManager.SetComponentData(hit.Entity,selected);
    } 
}

```

#### Collsion Filter 

Collision filters allow you to define which layers of objects should interact with each other.
- `CollisionFilter.BelongsTo` - often set to `~0u` to indicate the object belongs to all layers.
- `CollisionFilter.CollidesWith` - specifies `1u<<7u` which layers the object can collide with.
- `CollisionFilter.GroupIndex` - used to group `0` objects for custom collision rules.

```csharp

## Essential Components 🧱

### PhysicsCollider
Defines the collision shape of an entity.

```csharp
using Unity.Physics;
using Unity.Mathematics;

// Create a box collider
var boxCollider = BoxCollider.Create(
    new BoxGeometry
    {
        Center = float3.zero,
        Orientation = quaternion.identity,
        Size = new float3(1f, 1f, 1f)
    }
);

entityManager.AddComponentData(entity, new PhysicsCollider 
{ 
    Value = boxCollider 
});
```

### PhysicsMass
Controls mass properties for dynamic bodies.

```csharp
// Add mass component for dynamic physics
entityManager.AddComponentData(entity, PhysicsMass.CreateDynamic(
    massGeometry: boxCollider.Value,
    mass: 1.0f
));
```

### PhysicsVelocity
Manages linear and angular velocity.

```csharp
entityManager.AddComponentData(entity, new PhysicsVelocity
{
    Linear = new float3(0, 0, 5f),   // Move forward
    Angular = new float3(0, 1f, 0)   // Rotate around Y-axis
});
```

## Collision Detection 🔍

### Collision Events

Handle collisions using the collision event stream.

```csharp
using Unity.Physics;
using Unity.Physics.Systems;

[UpdateInGroup(typeof(FixedStepSimulationSystemGroup))]
[UpdateAfter(typeof(PhysicsSystemGroup))]
public partial class CollisionEventSystem : SystemBase
{
    private StepPhysicsWorld stepPhysicsWorld;
    
    protected override void OnCreate()
    {
        stepPhysicsWorld = World.GetOrCreateSystemManaged<StepPhysicsWorld>();
    }
    
    protected override void OnUpdate()
    {
        Dependency = new CollisionEventJob
        {
            // Component lookups
        }.Schedule(stepPhysicsWorld.Simulation, Dependency);
    }
}

public struct CollisionEventJob : ICollisionEventsJob
{
    public void Execute(CollisionEvent collisionEvent)
    {
        Entity entityA = collisionEvent.EntityA;
        Entity entityB = collisionEvent.EntityB;
        
        // Handle collision logic
        UnityEngine.Debug.Log($"Collision between {entityA} and {entityB}");
    }
}
```

### Raycast Operations ⚡
Perform efficient raycasts in ECS.

```csharp
using Unity.Physics;

public partial class RaycastSystem : SystemBase
{
    protected override void OnUpdate()
    {
        var physicsWorld = SystemAPI.GetSingleton<PhysicsWorldSingleton>().PhysicsWorld;
        
        var raycastInput = new RaycastInput
        {
            Start = new float3(0, 0, 0),
            End = new float3(0, -10, 0),
            Filter = CollisionFilter.Default
        };
        
        if (physicsWorld.CastRay(raycastInput, out RaycastHit hit))
        {
            // Ray hit something
            Entity hitEntity = physicsWorld.Bodies[hit.RigidBodyIndex].Entity;
            float3 hitPoint = hit.Position;
        }
    }
}
```

## Forces and Impulses 💥

### Applying Forces
Use `PhysicsVelocity` to apply forces and impulses.

```csharp
public partial class ForceApplicationSystem : SystemBase
{
    protected override void OnUpdate()
    {
        float deltaTime = SystemAPI.Time.DeltaTime;
        
        Entities.ForEach((ref PhysicsVelocity velocity, 
                         in PhysicsMass mass,
                         in ForceComponent force) =>
        {
            // Apply force (F = ma)
            velocity.Linear += force.Value * deltaTime / mass.InverseMass;
            
            // Apply impulse (direct velocity change)
            velocity.Linear += force.ImpulseValue / mass.InverseMass;
            
        }).Schedule();
    }
}

public struct ForceComponent : IComponentData
{
    public float3 Value;
    public float3 ImpulseValue;
}
```

## Joints and Constraints 🔗

### Distance Joint
Connect two bodies with a distance constraint.

```csharp
using Unity.Physics.Authoring;

// Create distance joint
var joint = PhysicsJoint.CreateDistanceJoint(
    new BodyFrame
    {
        Axis = new float3(0, 1, 0),
        PerpendicularAxis = new float3(1, 0, 0),
        Position = float3.zero
    },
    new BodyFrame  
    {
        Axis = new float3(0, 1, 0),
        PerpendicularAxis = new float3(1, 0, 0),
        Position = new float3(0, 2, 0)
    },
    minDistance: 0f,
    maxDistance: 3f
);

entityManager.AddComponentData(entity, new PhysicsJoint { Value = joint });
```

## Material Properties 🎨

### Physics Material
Define friction, restitution, and other surface properties.

```csharp
// Create physics material
var physicsMaterial = new Material
{
    Friction = 0.5f,
    Restitution = 0.8f,  // Bounciness
    FrictionCombinePolicy = Material.CombinePolicy.GeometricMean,
    RestitutionCombinePolicy = Material.CombinePolicy.Maximum
};

// Apply to collider
var colliderBlob = BoxCollider.Create(
    new BoxGeometry { Size = new float3(1) },
    filter: CollisionFilter.Default,
    material: physicsMaterial
);
```

## Advanced Features 🚀

### Custom Physics Step
Override physics simulation behavior.

```csharp
[UpdateInGroup(typeof(FixedStepSimulationSystemGroup))]
[UpdateBefore(typeof(PhysicsSystemGroup))]
public partial class CustomPhysicsStepSystem : SystemBase
{
    protected override void OnUpdate()
    {
        // Modify physics settings before simulation
        var physicsStep = SystemAPI.GetSingletonRW<PhysicsStep>();
        
        physicsStep.ValueRW.SolverIterationCount = 8;
        physicsStep.ValueRW.ThreadCountHint = 4;
        physicsStep.ValueRW.Gravity = new float3(0, -20f, 0); // Double gravity
    }
}
```

### Trigger Events
Handle trigger volume interactions.

```csharp
public struct TriggerEventJob : ITriggerEventsJob
{
    [ReadOnly] public ComponentLookup<PlayerTag> playerLookup;
    
    public void Execute(TriggerEvent triggerEvent)
    {
        Entity entityA = triggerEvent.EntityA;
        Entity entityB = triggerEvent.EntityB;
        
        // Check if player entered trigger
        if (playerLookup.HasComponent(entityA) || playerLookup.HasComponent(entityB))
        {
            // Handle trigger interaction
            UnityEngine.Debug.Log("Player entered trigger zone!");
        }
    }
}
```

## Performance Optimization ⚡

### Collision Layers
Use collision filtering to reduce unnecessary checks.

```csharp
public static class CollisionLayers
{
    public static readonly uint Player = 1u << 0;
    public static readonly uint Enemy = 1u << 1;
    public static readonly uint Environment = 1u << 2;
    public static readonly uint Projectile = 1u << 3;
}

// Create filtered collision
var filter = new CollisionFilter
{
    BelongsTo = CollisionLayers.Player,
    CollidesWith = CollisionLayers.Enemy | CollisionLayers.Environment
};
```

### Broadphase Optimization
Configure spatial partitioning for better performance.

```csharp
// In PhysicsStep component
var physicsStep = SystemAPI.GetSingletonRW<PhysicsStep>();
physicsStep.ValueRW.MultiThreaded = 1; // Enable multithreading
physicsStep.ValueRW.SolverIterationCount = 4; // Reduce for performance
```

## Common Patterns 🔄

### Object Pooling with Physics
Efficiently reuse physics entities.

```csharp
public partial class PhysicsPoolSystem : SystemBase
{
    private EntityQuery poolQuery;
    
    protected override void OnCreate()
    {
        poolQuery = GetEntityQuery(typeof(PooledPhysicsObject), typeof(PhysicsCollider));
    }
    
    public Entity GetPooledEntity()
    {
        var entities = poolQuery.ToEntityArray(Allocator.Temp);
        if (entities.Length > 0)
        {
            Entity entity = entities[0];
            
            // Reset physics state
            SystemAPI.SetComponent(entity, new PhysicsVelocity());
            SystemAPI.SetComponent(entity, LocalTransform.Identity);
            
            return entity;
        }
        
        return Entity.Null;
    }
}
```

## Best Practices ✨

1. **Use Static Bodies** for non-moving geometry to improve performance
2. **Batch Operations** when modifying multiple physics entities
3. **Limit Collision Queries** to necessary entities using filters
4. **Profile Physics Systems** to identify bottlenecks
5. **Use Appropriate Solver Settings** for your simulation needs

## Debugging Tips 🐛

### Physics Debug Draw
Visualize physics shapes and contacts.

```csharp
#if UNITY_EDITOR
using Unity.Physics.Authoring;

public partial class PhysicsDebugSystem : SystemBase
{
    protected override void OnUpdate()
    {
        if (HasSingleton<PhysicsDebugDisplayData>())
        {
            var debugData = SystemAPI.GetSingletonRW<PhysicsDebugDisplayData>();
            debugData.ValueRW.DrawColliders = 1;
            debugData.ValueRW.DrawColliderEdges = 1;
            debugData.ValueRW.DrawCollisionEvents = 1;
        }
    }
}
#endif
```

This comprehensive guide covers the essential aspects of Unity ECS Physics, from basic setup to advanced optimization techniques. The system provides excellent performance for physics-heavy applications while maintaining the benefits of the DOTS architecture.
