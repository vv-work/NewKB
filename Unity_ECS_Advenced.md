# Unity ECS Advanced Concepts

This document covers advanced Unity ECS patterns, optimizations, and complex scenarios for experienced developers.

## Table of Contents

1. [Advanced SystemAPI.Query](#advanced-systemapiquery)
2. [MonoBehaviour Integration](#monobehaviour-integration)
3. [Advanced Component Patterns](#advanced-component-patterns)
4. [System Dependencies and Ordering](#system-dependencies-and-ordering)
5. [Advanced Job Patterns](#advanced-job-patterns)
6. [Memory Optimization Strategies](#memory-optimization-strategies)
7. [Networking and Multiplayer](#networking-and-multiplayer)
8. [Advanced Aspects](#advanced-aspects)
9. [Chunk Iteration](#chunk-iteration)
10. [Custom Allocators](#custom-allocators)
11. [Reflection and Code Generation](#reflection-and-code-generation)
12. [Advanced Debugging](#advanced-debugging)

## Advanced SystemAPI.Query

### Complex Query Patterns

SystemAPI.Query provides powerful filtering and access patterns for complex scenarios.

```csharp
// Multiple component access with complex filtering
foreach (var (transform, health, weapon, entity) in 
         SystemAPI.Query<RefRW<LocalTransform>, RefRW<Health>, RefRO<Weapon>>()
                  .WithAll<PlayerTag, CombatEnabled>()
                  .WithAny<RangedWeapon, MeleeWeapon>()
                  .WithNone<DeadTag, StunnedTag>()
                  .WithEntityAccess())
{
    // Complex combat logic
    if (weapon.ValueRO.Ammo <= 0 && SystemAPI.HasComponent<RangedWeapon>(entity))
    {
        health.ValueRW.Current -= 10; // Out of ammo penalty
    }
}
```

### Query Caching and Reuse

```csharp
public partial struct OptimizedCombatSystem : ISystem
{
    private EntityQuery combatQuery;
    private EntityQuery deadEntitiesQuery;
    
    public void OnCreate(ref SystemState state)
    {
        // Cache queries for better performance
        combatQuery = SystemAPI.QueryBuilder()
            .WithAll<LocalTransform, Health, Weapon>()
            .WithAny<PlayerTag, EnemyTag>()
            .WithNone<DeadTag>()
            .Build();
            
        deadEntitiesQuery = SystemAPI.QueryBuilder()
            .WithAll<DeadTag>()
            .WithPresent<Health>() // Component exists but may be disabled
            .Build();
    }
    
    public void OnUpdate(ref SystemState state)
    {
        // Use cached queries
        int aliveCount = combatQuery.CalculateEntityCount();
        int deadCount = deadEntitiesQuery.CalculateEntityCount();
        
        if (aliveCount == 0) return; // No entities to process
    }
}
```

### Advanced Filtering with EntityQueryOptions

```csharp
public partial struct AdvancedQuerySystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // Include disabled entities in query
        foreach (var (health, entity) in 
                 SystemAPI.Query<RefRW<Health>>()
                          .WithEntityQueryOptions(EntityQueryOptions.IncludeDisabledEntities))
        {
            // Process even disabled entities
        }
        
        // Include prefab entities
        foreach (var prefabData in 
                 SystemAPI.Query<RefRO<PrefabData>>()
                          .WithEntityQueryOptions(EntityQueryOptions.IncludePrefab))
        {
            // Access prefab templates
        }
        
        // Filter by archetype changes
        foreach (var (transform, entity) in 
                 SystemAPI.Query<RefRW<LocalTransform>>()
                          .WithEntityQueryOptions(EntityQueryOptions.FilterWriteGroup)
                          .WithEntityAccess())
        {
            // Only process entities with specific archetype patterns
        }
    }
}
```

### Component Lookups for Complex Relationships

```csharp
public partial struct HierarchySystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var transformLookup = SystemAPI.GetComponentLookup<LocalTransform>(false);
        var parentLookup = SystemAPI.GetComponentLookup<Parent>(true);
        var childLookup = SystemAPI.GetBufferLookup<Child>(true);
        
        foreach (var (transform, entity) in 
                 SystemAPI.Query<RefRW<LocalTransform>>()
                          .WithAll<Parent>()
                          .WithEntityAccess())
        {
            var parent = parentLookup[entity];
            
            if (transformLookup.HasComponent(parent.Value))
            {
                var parentTransform = transformLookup[parent.Value];
                
                // Apply hierarchical transformation
                transform.ValueRW.Position = math.transform(
                    parentTransform.ToMatrix(),
                    transform.ValueRO.Position
                );
                
                // Process all children
                if (childLookup.HasBuffer(entity))
                {
                    var children = childLookup[entity];
                    for (int i = 0; i < children.Length; i++)
                    {
                        Entity child = children[i].Value;
                        if (transformLookup.HasComponent(child))
                        {
                            var childTransform = transformLookup[child];
                            // Update child...
                        }
                    }
                }
            }
        }
    }
}
```

## MonoBehaviour Integration

### Advanced Hybrid Workflows

```csharp
// ECS System that communicates with MonoBehaviour
public partial struct GameStateSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var gameState = SystemAPI.GetSingleton<GameState>();
        
        // Find MonoBehaviour component in scene
        var uiManager = UnityEngine.Object.FindObjectOfType<UIManager>();
        if (uiManager != null)
        {
            uiManager.UpdateHealthBar(gameState.PlayerHealth, gameState.MaxPlayerHealth);
            uiManager.UpdateScore(gameState.Score);
        }
    }
}

// MonoBehaviour that creates ECS entities
public class EnemySpawnerMB : MonoBehaviour
{
    public GameObject enemyPrefab;
    public int spawnCount = 10;
    
    void Start()
    {
        var world = World.DefaultGameObjectInjectionWorld;
        var entityManager = world.EntityManager;
        
        // Convert GameObject to Entity prefab
        var entityPrefab = GameObjectConversionUtility.ConvertGameObjectHierarchy(
            enemyPrefab, world);
        
        // Create spawner entity
        var spawnerEntity = entityManager.CreateEntity();
        entityManager.AddComponentData(spawnerEntity, new EnemySpawner
        {
            Prefab = entityPrefab,
            Count = spawnCount,
            SpawnRate = 1.0f
        });
    }
}
```

### Managed Component Bridge

```csharp
// Managed component for complex data
public class ManagedGameObjectReference : IComponentData
{
    public GameObject GameObject;
    public Animator Animator;
    public AudioSource AudioSource;
}

public partial struct ManagedComponentSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (health, managedRef) in 
                 SystemAPI.Query<RefRO<Health>, ManagedGameObjectReference>())
        {
            if (health.ValueRO.Current <= 0)
            {
                // Trigger death animation
                if (managedRef.Animator != null)
                {
                    managedRef.Animator.SetTrigger("Death");
                }
                
                // Play death sound
                if (managedRef.AudioSource != null)
                {
                    managedRef.AudioSource.PlayOneShot(deathClip);
                }
            }
        }
    }
}
```

## Advanced Component Patterns

### State Machine Components

```csharp
public enum AIState : byte
{
    Idle,
    Patrol,
    Chase,
    Attack,
    Flee,
    Dead
}

public struct AIStateMachine : IComponentData
{
    public AIState CurrentState;
    public AIState PreviousState;
    public float StateTimer;
    public float StateTransitionCooldown;
}

public struct AIStateTransition : IBufferElementData
{
    public AIState FromState;
    public AIState ToState;
    public float Probability;
    public float MinDuration;
}

public partial struct AIStateMachineSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var deltaTime = SystemAPI.Time.DeltaTime;
        
        foreach (var (stateMachine, transitions, entity) in 
                 SystemAPI.Query<RefRW<AIStateMachine>, DynamicBuffer<AIStateTransition>>()
                          .WithEntityAccess())
        {
            stateMachine.ValueRW.StateTimer += deltaTime;
            
            // Check for state transitions
            if (stateMachine.ValueRO.StateTimer > stateMachine.ValueRO.StateTransitionCooldown)
            {
                var currentState = stateMachine.ValueRO.CurrentState;
                
                for (int i = 0; i < transitions.Length; i++)
                {
                    var transition = transitions[i];
                    if (transition.FromState == currentState &&
                        stateMachine.ValueRO.StateTimer >= transition.MinDuration)
                    {
                        if (UnityEngine.Random.value < transition.Probability)
                        {
                            stateMachine.ValueRW.PreviousState = currentState;
                            stateMachine.ValueRW.CurrentState = transition.ToState;
                            stateMachine.ValueRW.StateTimer = 0;
                            break;
                        }
                    }
                }
            }
        }
    }
}
```

### Component Composition Patterns

```csharp
// Composition over inheritance
public struct Attackable : IComponentData
{
    public float Damage;
    public float Range;
    public float Cooldown;
    public float LastAttackTime;
}

public struct Moveable : IComponentData
{
    public float Speed;
    public float AccelerationTime;
    public float DecelerationTime;
}

public struct Targetable : IComponentData
{
    public float3 LastKnownPosition;
    public Entity CurrentTarget;
    public float DetectionRange;
    public float LostTargetTime;
}

// Entity archetypes using composition
public static class EntityArchetypes
{
    public static EntityArchetype CreateMeleeWarrior(EntityManager entityManager)
    {
        return entityManager.CreateArchetype(
            typeof(LocalTransform),
            typeof(Health),
            typeof(Attackable),
            typeof(Moveable),
            typeof(Targetable),
            typeof(MeleeWeapon),
            typeof(WarriorTag)
        );
    }
    
    public static EntityArchetype CreateRangedArcher(EntityManager entityManager)
    {
        return entityManager.CreateArchetype(
            typeof(LocalTransform),
            typeof(Health),
            typeof(Attackable),
            typeof(Moveable),
            typeof(Targetable),
            typeof(RangedWeapon),
            typeof(ArcherTag)
        );
    }
}
```

### Dynamic Component Management

```csharp
public partial struct DynamicComponentSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var ecb = SystemAPI.GetSingleton<EndSimulationEntityCommandBufferSystem.Singleton>()
                           .CreateCommandBuffer(state.WorldUnmanaged);
        
        foreach (var (health, equipment, entity) in 
                 SystemAPI.Query<RefRO<Health>, DynamicBuffer<Equipment>>()
                          .WithEntityAccess())
        {
            // Add temporary components based on equipment
            for (int i = 0; i < equipment.Length; i++)
            {
                var item = equipment[i];
                
                switch (item.Type)
                {
                    case EquipmentType.SpeedBoost:
                        if (!SystemAPI.HasComponent<SpeedBuff>(entity))
                        {
                            ecb.AddComponent(entity, new SpeedBuff 
                            { 
                                Multiplier = item.Value,
                                Duration = item.Duration 
                            });
                        }
                        break;
                        
                    case EquipmentType.Shield:
                        if (!SystemAPI.HasComponent<DamageReduction>(entity))
                        {
                            ecb.AddComponent(entity, new DamageReduction 
                            { 
                                Percentage = item.Value 
                            });
                        }
                        break;
                }
            }
        }
        
        // Remove expired temporary components
        foreach (var (speedBuff, entity) in 
                 SystemAPI.Query<RefRW<SpeedBuff>>().WithEntityAccess())
        {
            speedBuff.ValueRW.Duration -= SystemAPI.Time.DeltaTime;
            if (speedBuff.ValueRO.Duration <= 0)
            {
                ecb.RemoveComponent<SpeedBuff>(entity);
            }
        }
    }
}
```

## System Dependencies and Ordering

### Complex System Groups

```csharp
[UpdateInGroup(typeof(InitializationSystemGroup), OrderFirst = true)]
public class InputSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateAfter(typeof(InputSystemGroup))]
public class GameLogicSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(GameLogicSystemGroup))]
public class AISystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(GameLogicSystemGroup))]
[UpdateAfter(typeof(AISystemGroup))]
public class PhysicsSystemGroup : ComponentSystemGroup { }

[UpdateInGroup(typeof(GameLogicSystemGroup))]
[UpdateAfter(typeof(PhysicsSystemGroup))]
public class RenderingSystemGroup : ComponentSystemGroup { }
```

### System Dependencies with JobHandle

```csharp
public partial struct PhysicsSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // Schedule physics job
        var physicsJob = new PhysicsJob
        {
            deltaTime = SystemAPI.Time.DeltaTime
        };
        
        state.Dependency = physicsJob.ScheduleParallel(state.Dependency);
    }
}

public partial struct RenderingSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // Wait for physics to complete before rendering
        state.Dependency.Complete();
        
        var renderJob = new UpdateRenderDataJob
        {
            // Rendering data
        };
        
        state.Dependency = renderJob.Schedule(state.Dependency);
    }
}
```

### Conditional System Execution

```csharp
public partial struct ConditionalSystem : ISystem
{
    private EntityQuery requiredQuery;
    
    public void OnCreate(ref SystemState state)
    {
        requiredQuery = SystemAPI.QueryBuilder()
            .WithAll<GameActive, PlayerAlive>()
            .WithNone<GamePaused>()
            .Build();
            
        state.RequireForUpdate(requiredQuery);
    }
    
    public void OnUpdate(ref SystemState state)
    {
        // Only runs when game is active, player is alive, and game is not paused
        if (!SystemAPI.HasSingleton<GameSettings>()) return;
        
        var settings = SystemAPI.GetSingleton<GameSettings>();
        if (!settings.EnableAI) return;
        
        // AI logic here...
    }
}
```

## Advanced Job Patterns

### Complex Job Chains

```csharp
[BurstCompile]
public partial struct ComplexSimulationJob : IJobEntity
{
    public float deltaTime;
    [ReadOnly] public ComponentLookup<Obstacle> obstacleLookup;
    [ReadOnly] public ComponentLookup<LocalTransform> transformLookup;
    
    public void Execute(ref LocalTransform transform, 
                       ref Velocity velocity, 
                       in MovementSettings settings)
    {
        // Complex movement with obstacle avoidance
        float3 avoidanceForce = CalculateAvoidanceForce(
            transform.Position, velocity.Value, obstacleLookup, transformLookup);
        
        velocity.Value += avoidanceForce * deltaTime;
        velocity.Value = math.clamp(velocity.Value, -settings.MaxSpeed, settings.MaxSpeed);
        
        transform.Position += velocity.Value * deltaTime;
    }
    
    private float3 CalculateAvoidanceForce(float3 position, float3 velocity,
        ComponentLookup<Obstacle> obstacles, ComponentLookup<LocalTransform> transforms)
    {
        // Implement complex avoidance algorithm
        return float3.zero;
    }
}

public partial struct SimulationSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        // Update transforms from previous frame lookups
        var transformLookup = SystemAPI.GetComponentLookup<LocalTransform>(true);
        var obstacleLookup = SystemAPI.GetComponentLookup<Obstacle>(true);
        
        var job = new ComplexSimulationJob
        {
            deltaTime = SystemAPI.Time.DeltaTime,
            transformLookup = transformLookup,
            obstacleLookup = obstacleLookup
        };
        
        state.Dependency = job.ScheduleParallel(state.Dependency);
    }
}
```

### Multi-Phase Processing

```csharp
[BurstCompile]
public struct GatherDataJob : IJobEntity
{
    public NativeArray<float3> positions;
    public NativeArray<float> healths;
    
    public void Execute([EntityIndexInQuery] int index, 
                       in LocalTransform transform, 
                       in Health health)
    {
        positions[index] = transform.Position;
        healths[index] = health.Current;
    }
}

[BurstCompile]
public struct ProcessDataJob : IJob
{
    public NativeArray<float3> positions;
    public NativeArray<float> healths;
    public NativeArray<float3> results;
    
    public void Execute()
    {
        // Complex processing of all entity data
        for (int i = 0; i < positions.Length; i++)
        {
            float3 avgPosition = CalculateAveragePosition(positions, i);
            float healthFactor = healths[i] / 100.0f;
            results[i] = math.lerp(positions[i], avgPosition, healthFactor);
        }
    }
    
    private float3 CalculateAveragePosition(NativeArray<float3> positions, int excludeIndex)
    {
        float3 sum = float3.zero;
        int count = 0;
        
        for (int i = 0; i < positions.Length; i++)
        {
            if (i != excludeIndex)
            {
                sum += positions[i];
                count++;
            }
        }
        
        return count > 0 ? sum / count : float3.zero;
    }
}

[BurstCompile]
public struct ApplyResultsJob : IJobEntity
{
    [ReadOnly] public NativeArray<float3> results;
    
    public void Execute([EntityIndexInQuery] int index, ref LocalTransform transform)
    {
        transform.Position = results[index];
    }
}

public partial struct MultiPhaseSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var query = SystemAPI.QueryBuilder()
            .WithAll<LocalTransform, Health>()
            .Build();
            
        int entityCount = query.CalculateEntityCount();
        if (entityCount == 0) return;
        
        using var positions = new NativeArray<float3>(entityCount, Allocator.TempJob);
        using var healths = new NativeArray<float>(entityCount, Allocator.TempJob);
        using var results = new NativeArray<float3>(entityCount, Allocator.TempJob);
        
        // Phase 1: Gather data
        var gatherJob = new GatherDataJob
        {
            positions = positions,
            healths = healths
        };
        var gatherHandle = gatherJob.ScheduleParallel(query, state.Dependency);
        
        // Phase 2: Process data
        var processJob = new ProcessDataJob
        {
            positions = positions,
            healths = healths,
            results = results
        };
        var processHandle = processJob.Schedule(gatherHandle);
        
        // Phase 3: Apply results
        var applyJob = new ApplyResultsJob
        {
            results = results
        };
        state.Dependency = applyJob.ScheduleParallel(query, processHandle);
    }
}
```

## Memory Optimization Strategies

### Object Pooling with ECS

```csharp
public struct PooledEntity : IComponentData
{
    public int PoolIndex;
    public bool IsActive;
}

public struct EntityPool : IComponentData
{
    public Entity PoolPrefab;
    public int PoolSize;
    public int ActiveCount;
}

public partial struct EntityPoolSystem : ISystem
{
    private NativeList<Entity> availableEntities;
    
    public void OnCreate(ref SystemState state)
    {
        availableEntities = new NativeList<Entity>(1000, Allocator.Persistent);
    }
    
    public void OnDestroy(ref SystemState state)
    {
        if (availableEntities.IsCreated)
            availableEntities.Dispose();
    }
    
    public void OnUpdate(ref SystemState state)
    {
        // Return inactive entities to pool
        foreach (var (pooled, entity) in 
                 SystemAPI.Query<RefRW<PooledEntity>>()
                          .WithEntityAccess())
        {
            if (!pooled.ValueRO.IsActive)
            {
                // Deactivate entity instead of destroying
                SystemAPI.SetComponentEnabled<LocalTransform>(entity, false);
                SystemAPI.SetComponentEnabled<Velocity>(entity, false);
                availableEntities.Add(entity);
                
                pooled.ValueRW.IsActive = false;
            }
        }
    }
    
    public Entity GetPooledEntity(ref SystemState state)
    {
        if (availableEntities.Length > 0)
        {
            var entity = availableEntities[availableEntities.Length - 1];
            availableEntities.RemoveAt(availableEntities.Length - 1);
            
            // Reactivate entity
            SystemAPI.SetComponentEnabled<LocalTransform>(entity, true);
            SystemAPI.SetComponentEnabled<Velocity>(entity, true);
            SystemAPI.SetComponentData(entity, new PooledEntity { IsActive = true });
            
            return entity;
        }
        
        // Create new entity if pool is empty
        return SystemAPI.EntityManager.CreateEntity();
    }
}
```

### Memory-Efficient Data Structures

```csharp
// Pack data efficiently using bit fields
public struct PackedUnitData : IComponentData
{
    // Using bit fields to pack data
    private uint packedData;
    
    public int Health
    {
        get => (int)(packedData & 0xFF);
        set => packedData = (packedData & ~0xFFu) | ((uint)value & 0xFF);
    }
    
    public int Level
    {
        get => (int)((packedData >> 8) & 0xFF);
        set => packedData = (packedData & ~(0xFFu << 8)) | (((uint)value & 0xFF) << 8);
    }
    
    public int Experience
    {
        get => (int)((packedData >> 16) & 0xFFFF);
        set => packedData = (packedData & ~(0xFFFFu << 16)) | (((uint)value & 0xFFFF) << 16);
    }
}

// Use smaller data types when possible
public struct CompactTransform : IComponentData
{
    public half3 Position;    // 6 bytes instead of 12
    public half Rotation;     // 2 bytes instead of 16 for quaternion
    public half Scale;        // 2 bytes instead of 4
}
```

## Networking and Multiplayer

### Client-Server Architecture

```csharp
public struct NetworkedEntity : IComponentData
{
    public uint NetworkId;
    public byte OwnerId;
    public bool IsDirty;
}

public struct ServerAuthoritative : IComponentData { }
public struct ClientPredicted : IComponentData { }

public partial struct NetworkSyncSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        if (IsServer())
        {
            // Server: Sync authoritative data to clients
            foreach (var (networked, transform, health) in 
                     SystemAPI.Query<RefRW<NetworkedEntity>, RefRO<LocalTransform>, RefRO<Health>>()
                              .WithAll<ServerAuthoritative>())
            {
                if (networked.ValueRO.IsDirty)
                {
                    SendNetworkUpdate(networked.ValueRO.NetworkId, transform.ValueRO, health.ValueRO);
                    networked.ValueRW.IsDirty = false;
                }
            }
        }
        else
        {
            // Client: Apply received updates
            ProcessNetworkUpdates(ref state);
            
            // Client prediction for local entities
            foreach (var (transform, velocity) in 
                     SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>()
                              .WithAll<ClientPredicted>())
            {
                transform.ValueRW.Position += velocity.ValueRO.Value * SystemAPI.Time.DeltaTime;
            }
        }
    }
    
    private bool IsServer() => SystemAPI.HasSingleton<ServerConfig>();
    
    private void SendNetworkUpdate(uint networkId, LocalTransform transform, Health health)
    {
        // Implementation depends on networking solution
    }
    
    private void ProcessNetworkUpdates(ref SystemState state)
    {
        // Implementation depends on networking solution
    }
}
```

### State Reconciliation

```csharp
public struct PredictionState : IBufferElementData
{
    public uint Tick;
    public float3 Position;
    public float3 Velocity;
    public uint InputSequence;
}

public partial struct ClientPredictionSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        uint currentTick = GetCurrentTick();
        
        foreach (var (transform, velocity, predictions, networked) in 
                 SystemAPI.Query<RefRW<LocalTransform>, RefRW<Velocity>, 
                                DynamicBuffer<PredictionState>, RefRO<NetworkedEntity>>()
                          .WithAll<ClientPredicted>())
        {
            // Store prediction state
            predictions.Add(new PredictionState
            {
                Tick = currentTick,
                Position = transform.ValueRO.Position,
                Velocity = velocity.ValueRO.Value,
                InputSequence = GetCurrentInputSequence()
            });
            
            // Remove old predictions (keep last 60)
            while (predictions.Length > 60)
            {
                predictions.RemoveAt(0);
            }
        }
    }
    
    public void OnServerStateReceived(uint networkId, uint serverTick, 
                                     float3 serverPosition, float3 serverVelocity)
    {
        // Find entity with matching network ID
        foreach (var (transform, velocity, predictions, networked) in 
                 SystemAPI.Query<RefRW<LocalTransform>, RefRW<Velocity>, 
                                DynamicBuffer<PredictionState>, RefRO<NetworkedEntity>>())
        {
            if (networked.ValueRO.NetworkId == networkId)
            {
                // Find matching prediction
                for (int i = 0; i < predictions.Length; i++)
                {
                    if (predictions[i].Tick == serverTick)
                    {
                        var prediction = predictions[i];
                        float3 error = serverPosition - prediction.Position;
                        
                        // Apply correction if error is significant
                        if (math.lengthsq(error) > 0.01f)
                        {
                            // Snap to server position and replay inputs
                            transform.ValueRW.Position = serverPosition;
                            velocity.ValueRW.Value = serverVelocity;
                            
                            // Replay all inputs after this tick
                            ReplayInputsFromTick(serverTick + 1, ref transform.ValueRW, ref velocity.ValueRW);
                        }
                        break;
                    }
                }
            }
        }
    }
    
    private uint GetCurrentTick() => (uint)(SystemAPI.Time.ElapsedTime * 60); // 60 Hz
    private uint GetCurrentInputSequence() => 0; // Implementation specific
    private void ReplayInputsFromTick(uint tick, ref LocalTransform transform, ref Velocity velocity) { }
}
```

## Advanced Aspects

### Hierarchical Aspects

```csharp
public readonly partial struct HierarchyAspect : IAspect
{
    readonly RefRW<LocalTransform> localTransform;
    readonly RefRO<Parent> parent;
    readonly DynamicBuffer<Child> children;
    
    [Optional] readonly RefRO<LocalToWorld> localToWorld;
    
    public float4x4 WorldMatrix => localToWorld.IsValid 
        ? localToWorld.ValueRO.Value 
        : localTransform.ValueRO.ToMatrix();
    
    public void SetWorldPosition(float3 worldPosition, 
                                ComponentLookup<LocalTransform> transformLookup)
    {
        if (parent.IsValid && transformLookup.HasComponent(parent.ValueRO.Value))
        {
            var parentTransform = transformLookup[parent.ValueRO.Value];
            var parentMatrix = parentTransform.ToMatrix();
            var localPosition = math.transform(math.inverse(parentMatrix), worldPosition);
            localTransform.ValueRW.Position = localPosition;
        }
        else
        {
            localTransform.ValueRW.Position = worldPosition;
        }
    }
    
    public void UpdateChildrenRecursive(ComponentLookup<LocalTransform> transformLookup, 
                                       ComponentLookup<LocalToWorld> worldLookup)
    {
        var worldMatrix = WorldMatrix;
        
        for (int i = 0; i < children.Length; i++)
        {
            var childEntity = children[i].Value;
            
            if (transformLookup.HasComponent(childEntity))
            {
                var childLocalTransform = transformLookup[childEntity];
                var childWorldMatrix = math.mul(worldMatrix, childLocalTransform.ToMatrix());
                
                if (worldLookup.HasComponent(childEntity))
                {
                    worldLookup[childEntity] = new LocalToWorld { Value = childWorldMatrix };
                }
            }
        }
    }
}
```

### Aspect Composition

```csharp
public readonly partial struct CombatAspect : IAspect
{
    readonly RefRW<Health> health;
    readonly RefRW<Weapon> weapon;
    readonly RefRO<CombatStats> stats;
    
    public bool IsAlive => health.ValueRO.Current > 0;
    public bool CanAttack => weapon.ValueRO.Cooldown <= 0 && weapon.ValueRO.Ammo > 0;
    
    public void TakeDamage(float damage)
    {
        float reducedDamage = damage * (1.0f - stats.ValueRO.DamageReduction);
        health.ValueRW.Current = math.max(0, health.ValueRO.Current - reducedDamage);
    }
    
    public bool TryAttack(float deltaTime, out float damageDealt)
    {
        damageDealt = 0;
        
        if (!CanAttack) return false;
        
        damageDealt = weapon.ValueRO.BaseDamage * stats.ValueRO.DamageMultiplier;
        weapon.ValueRW.Cooldown = weapon.ValueRO.AttackSpeed;
        weapon.ValueRW.Ammo--;
        
        return true;
    }
}

public readonly partial struct MovementAspect : IAspect
{
    readonly RefRW<LocalTransform> transform;
    readonly RefRW<Velocity> velocity;
    readonly RefRO<MovementStats> stats;
    
    public float3 Position
    {
        get => transform.ValueRO.Position;
        set => transform.ValueRW.Position = value;
    }
    
    public void MoveTowards(float3 targetPosition, float deltaTime)
    {
        float3 direction = math.normalize(targetPosition - Position);
        float3 desiredVelocity = direction * stats.ValueRO.MaxSpeed;
        
        velocity.ValueRW.Value = math.lerp(
            velocity.ValueRO.Value, 
            desiredVelocity, 
            stats.ValueRO.Acceleration * deltaTime
        );
        
        Position += velocity.ValueRO.Value * deltaTime;
    }
}

// Composite aspect using multiple aspects
public readonly partial struct UnitAspect : IAspect
{
    readonly CombatAspect combat;
    readonly MovementAspect movement;
    readonly RefRO<AIState> aiState;
    
    public bool ShouldFlee => combat.health.ValueRO.Current < (combat.health.ValueRO.Maximum * 0.2f);
    
    public void UpdateBehavior(float deltaTime, float3 targetPosition)
    {
        if (!combat.IsAlive) return;
        
        switch (aiState.ValueRO.CurrentState)
        {
            case AIStateType.Chase:
                movement.MoveTowards(targetPosition, deltaTime);
                break;
                
            case AIStateType.Attack:
                if (combat.TryAttack(deltaTime, out float damage))
                {
                    // Deal damage to target
                }
                break;
                
            case AIStateType.Flee:
                float3 fleeDirection = math.normalize(movement.Position - targetPosition);
                float3 fleeTarget = movement.Position + fleeDirection * 10.0f;
                movement.MoveTowards(fleeTarget, deltaTime);
                break;
        }
    }
}
```

## Chunk Iteration

### Manual Chunk Processing

```csharp
public partial struct ChunkIterationSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var query = SystemAPI.QueryBuilder()
            .WithAll<LocalTransform, Velocity>()
            .WithNone<Static>()
            .Build();
            
        var transformType = SystemAPI.GetComponentTypeHandle<LocalTransform>(false);
        var velocityType = SystemAPI.GetComponentTypeHandle<Velocity>(true);
        
        var chunks = query.ToArchetypeChunkArray(Allocator.TempJob);
        
        for (int chunkIndex = 0; chunkIndex < chunks.Length; chunkIndex++)
        {
            var chunk = chunks[chunkIndex];
            
            var transforms = chunk.GetNativeArray(ref transformType);
            var velocities = chunk.GetNativeArray(ref velocityType);
            
            // Process entire chunk in batch
            for (int entityIndex = 0; entityIndex < chunk.Count; entityIndex++)
            {
                var transform = transforms[entityIndex];
                var velocity = velocities[entityIndex];
                
                transform.Position += velocity.Value * SystemAPI.Time.DeltaTime;
                transforms[entityIndex] = transform;
            }
        }
        
        chunks.Dispose();
    }
}
```

### Chunk-Based Job Processing

```csharp
[BurstCompile]
public struct ChunkJob : IJobChunk
{
    public ComponentTypeHandle<LocalTransform> TransformTypeHandle;
    [ReadOnly] public ComponentTypeHandle<Velocity> VelocityTypeHandle;
    [ReadOnly] public float DeltaTime;
    
    public void Execute(in ArchetypeChunk chunk, int unfilteredChunkIndex, 
                       bool useEnabledMask, in v128 chunkEnabledMask)
    {
        var transforms = chunk.GetNativeArray(ref TransformTypeHandle);
        var velocities = chunk.GetNativeArray(ref VelocityTypeHandle);
        
        for (int i = 0; i < chunk.Count; i++)
        {
            if (useEnabledMask && !EnabledBitUtility.GetBit(chunkEnabledMask, i))
                continue;
                
            var transform = transforms[i];
            var velocity = velocities[i];
            
            transform.Position += velocity.Value * DeltaTime;
            transforms[i] = transform;
        }
    }
}

public partial struct ChunkJobSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var job = new ChunkJob
        {
            TransformTypeHandle = SystemAPI.GetComponentTypeHandle<LocalTransform>(false),
            VelocityTypeHandle = SystemAPI.GetComponentTypeHandle<Velocity>(true),
            DeltaTime = SystemAPI.Time.DeltaTime
        };
        
        var query = SystemAPI.QueryBuilder()
            .WithAll<LocalTransform, Velocity>()
            .Build();
            
        state.Dependency = job.ScheduleParallel(query, state.Dependency);
    }
}
```

## Custom Allocators

### Implementing Custom Allocators

```csharp
public struct StackAllocator : AllocatorManager.IAllocator
{
    private AllocatorManager.AllocatorHandle handle;
    private UnsafeList<byte> memory;
    private int position;
    
    public AllocatorManager.AllocatorHandle Handle => handle;
    
    public StackAllocator(int capacity)
    {
        handle = AllocatorManager.AllocatorHandle.Invalid;
        memory = new UnsafeList<byte>(capacity, Allocator.Persistent);
        position = 0;
        
        AllocatorManager.Initialize();
        handle = AllocatorManager.RegisterAllocator(this);
    }
    
    public AllocatorManager.TryFunction Function => TryAllocate;
    
    private AllocatorManager.AllocatorHandle TryAllocate(ref AllocatorManager.Block block)
    {
        if (block.Range.Pointer == IntPtr.Zero)
        {
            // Allocation
            if (position + (int)block.Range.Items > memory.Capacity)
            {
                return AllocatorManager.AllocatorHandle.Invalid;
            }
            
            unsafe
            {
                block.Range.Pointer = (IntPtr)(memory.Ptr + position);
            }
            position += (int)block.Range.Items;
            block.AllocatedItems = block.Range.Items;
        }
        else
        {
            // Deallocation - stack allocator only supports LIFO
            unsafe
            {
                byte* ptr = (byte*)block.Range.Pointer;
                if (ptr + block.Range.Items == memory.Ptr + position)
                {
                    position -= (int)block.Range.Items;
                }
            }
        }
        
        return handle;
    }
    
    public void Dispose()
    {
        if (handle.IsValid)
        {
            AllocatorManager.UnregisterAllocator(handle);
            handle = AllocatorManager.AllocatorHandle.Invalid;
        }
        
        if (memory.IsCreated)
        {
            memory.Dispose();
        }
    }
}

// Usage example
public partial struct CustomAllocatorSystem : ISystem
{
    private StackAllocator stackAllocator;
    
    public void OnCreate(ref SystemState state)
    {
        stackAllocator = new StackAllocator(1024 * 1024); // 1MB stack
    }
    
    public void OnDestroy(ref SystemState state)
    {
        stackAllocator.Dispose();
    }
    
    public void OnUpdate(ref SystemState state)
    {
        // Use custom allocator for temporary data
        using var tempArray = new NativeArray<float3>(100, stackAllocator.Handle);
        
        // Process data...
    }
}
```

## Reflection and Code Generation

### Runtime Component Discovery

```csharp
public static class ComponentDiscovery
{
    private static readonly Dictionary<Type, ComponentType> componentTypes = 
        new Dictionary<Type, ComponentType>();
    
    static ComponentDiscovery()
    {
        DiscoverComponentTypes();
    }
    
    private static void DiscoverComponentTypes()
    {
        var assemblies = System.AppDomain.CurrentDomain.GetAssemblies();
        
        foreach (var assembly in assemblies)
        {
            var types = assembly.GetTypes()
                .Where(t => typeof(IComponentData).IsAssignableFrom(t) && !t.IsAbstract);
            
            foreach (var type in types)
            {
                componentTypes[type] = ComponentType.ReadWrite(type);
            }
        }
    }
    
    public static ComponentType GetComponentType<T>() where T : struct, IComponentData
    {
        return componentTypes.TryGetValue(typeof(T), out var componentType) 
            ? componentType 
            : ComponentType.ReadWrite<T>();
    }
    
    public static EntityArchetype CreateArchetypeFromNames(EntityManager entityManager, 
                                                          params string[] componentNames)
    {
        var componentTypes = new List<ComponentType>();
        
        foreach (var name in componentNames)
        {
            var type = Type.GetType(name);
            if (type != null && componentTypes.ContainsKey(type))
            {
                componentTypes.Add(componentTypes[type]);
            }
        }
        
        return entityManager.CreateArchetype(componentTypes.ToArray());
    }
}
```

### Dynamic System Creation

```csharp
public abstract class DynamicSystemBase : SystemBase
{
    protected abstract void OnUpdateDynamic();
    
    protected override void OnUpdate() => OnUpdateDynamic();
}

public class DynamicSystemFactory
{
    public static SystemHandle CreateSystem<T>(World world, string systemName = null) 
        where T : DynamicSystemBase, new()
    {
        var system = new T();
        return world.AddSystemManaged(system);
    }
    
    public static void CreateSystemFromConfig(World world, SystemConfig config)
    {
        var systemType = Type.GetType(config.TypeName);
        if (systemType != null && typeof(DynamicSystemBase).IsAssignableFrom(systemType))
        {
            var system = (DynamicSystemBase)Activator.CreateInstance(systemType);
            world.AddSystemManaged(system);
        }
    }
}

[Serializable]
public struct SystemConfig
{
    public string TypeName;
    public string GroupName;
    public bool Enabled;
    public float UpdateRate;
}
```

## Advanced Debugging

### Custom Entity Inspector

```csharp
#if UNITY_EDITOR
using UnityEditor;

[System.Serializable]
public class EntityInspector
{
    private Entity selectedEntity;
    private World selectedWorld;
    
    public void DrawInspector()
    {
        GUILayout.Label("Entity Inspector", EditorStyles.boldLabel);
        
        // World selection
        var worlds = new List<World>();
        foreach (var world in World.All)
        {
            worlds.Add(world);
        }
        
        if (worlds.Count > 0)
        {
            var worldNames = worlds.Select(w => w.Name).ToArray();
            int selectedIndex = worlds.IndexOf(selectedWorld);
            selectedIndex = EditorGUILayout.Popup("World", selectedIndex, worldNames);
            
            if (selectedIndex >= 0 && selectedIndex < worlds.Count)
            {
                selectedWorld = worlds[selectedIndex];
                DrawEntityList();
            }
        }
    }
    
    private void DrawEntityList()
    {
        if (selectedWorld == null || !selectedWorld.IsCreated) return;
        
        var entityManager = selectedWorld.EntityManager;
        var allEntities = entityManager.GetAllEntities(Allocator.Temp);
        
        GUILayout.Label($"Entities ({allEntities.Length})", EditorStyles.boldLabel);
        
        for (int i = 0; i < math.min(allEntities.Length, 100); i++) // Limit display
        {
            var entity = allEntities[i];
            
            if (GUILayout.Button($"Entity {entity.Index}:{entity.Version}"))
            {
                selectedEntity = entity;
            }
            
            if (selectedEntity.Equals(entity))
            {
                DrawEntityDetails(entity, entityManager);
            }
        }
        
        allEntities.Dispose();
    }
    
    private void DrawEntityDetails(Entity entity, EntityManager entityManager)
    {
        EditorGUI.indentLevel++;
        
        if (!entityManager.Exists(entity))
        {
            GUILayout.Label("Entity no longer exists");
            EditorGUI.indentLevel--;
            return;
        }
        
        // Show archetype
        var archetype = entityManager.GetArchetype(entity);
        GUILayout.Label($"Archetype: {archetype}");
        
        // Show components
        var componentTypes = archetype.GetComponentTypes();
        
        foreach (var componentType in componentTypes)
        {
            GUILayout.Label($"- {componentType.GetManagedType().Name}");
            
            // Show component data if possible
            if (componentType.IsComponentData && !componentType.IsZeroSized)
            {
                DrawComponentData(entity, componentType, entityManager);
            }
        }
        
        componentTypes.Dispose();
        EditorGUI.indentLevel--;
    }
    
    private void DrawComponentData(Entity entity, ComponentType componentType, 
                                  EntityManager entityManager)
    {
        // This would need reflection or codegen to show actual values
        EditorGUI.indentLevel++;
        GUILayout.Label("  [Component data display would go here]");
        EditorGUI.indentLevel--;
    }
}

[UnityEditor.CustomEditor(typeof(ConversionScene))]
public class EntityInspectorWindow : EditorWindow
{
    private EntityInspector inspector = new EntityInspector();
    
    [MenuItem("Window/ECS/Entity Inspector")]
    public static void ShowWindow()
    {
        GetWindow<EntityInspectorWindow>("Entity Inspector");
    }
    
    private void OnGUI()
    {
        inspector.DrawInspector();
    }
}
#endif
```

### Performance Profiling Tools

```csharp
public static class ECSProfiler
{
    private static readonly Dictionary<string, float> systemTimes = 
        new Dictionary<string, float>();
    
    public static void BeginSample(string sampleName)
    {
        UnityEngine.Profiling.Profiler.BeginSample(sampleName);
    }
    
    public static void EndSample()
    {
        UnityEngine.Profiling.Profiler.EndSample();
    }
    
    public static void RecordSystemTime(string systemName, float time)
    {
        systemTimes[systemName] = time;
    }
    
    public static void LogSystemTimes()
    {
        var sortedTimes = systemTimes.OrderByDescending(kvp => kvp.Value);
        
        UnityEngine.Debug.Log("System Performance Report:");
        foreach (var kvp in sortedTimes.Take(10))
        {
            UnityEngine.Debug.Log($"{kvp.Key}: {kvp.Value:F3}ms");
        }
    }
}

// Usage in systems
public partial struct ProfiledSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        var startTime = UnityEngine.Time.realtimeSinceStartup;
        ECSProfiler.BeginSample("ProfiledSystem.OnUpdate");
        
        // System logic here...
        
        ECSProfiler.EndSample();
        var elapsed = (UnityEngine.Time.realtimeSinceStartup - startTime) * 1000;
        ECSProfiler.RecordSystemTime("ProfiledSystem", elapsed);
    }
}
```

This comprehensive advanced guide covers sophisticated Unity ECS patterns and techniques for complex game development scenarios. Use these patterns when building large-scale, performance-critical applications that require advanced entity management, networking, and optimization strategies.