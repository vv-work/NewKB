# Unity ECS Advanced Concepts


## SystemAPI 

```csharp

Entity entity =  SystemAPI.GetSingletonEntity<InputState>();
InputState inputState = SystemAPI.GetSingleton<InputState>();
float deltaTime = SystemAPI.Time.DeltaTime;
```

### quaternion

```csharp
quaternion rotation = quaternion.EulerXYZ(0, 0, 0); // Create
```


## Organizational tags 

```csharp
[UpdateInGroup(typeof(InitializationSystemGroup), OrderLast = true)] //Intilize in System group
[UpdateBefore(typeof(PlayerShootingSystem))]               // Update before PlayerShootingSystem
```

## Making Singleton for input System

```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateBefore(typeof(PlayerShootingSystem))] 
public partial class PlayerInputSystem : SystemBase 
{
    protected override void OnCreate()
    {
        base.OnCreate(); 
        // Ensure an InputState singleton exists
        EntityQuery q = GetEntityQuery(ComponentType.ReadOnly<InputState>());
        if (q.IsEmptyIgnoreFilter)
        {
            Entity e = EntityManager.CreateEntity(typeof(InputState));
            EntityManager.SetName(e, "InputStateSingleton");
            EntityManager.SetComponentData(e, new InputState { ShootTriggered = false });
        }
    } 
```

