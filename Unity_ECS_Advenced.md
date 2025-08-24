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

## Getting reference from MonoBehaviour to Entity 

```csharp
    VisualEntity = GetEntity(authoring.VisualEntity, TransformUsageFlags.Dynamic)
```


## MonoBehaviour getting Entity Reference 



```csharp

private void Update(){
     EntityManager entityManager =  World.DefaultGameObjectInjectionWorld.EntityManager;
     EntityQuery entityQuery = new EntityQueryBuilder(Allocator.Temp).WithAll<UnitMoverData>().Build(entityManager);
}

```
### Query ToEntityArray and to ToComponentDataArray

- `ToEntityArray(Allocator.Temp)` - getting NativeArray of `Entiti`'s from entityQuery
- `ToComponentDataArray<UnitMoverData>(Allocator.Temp)` - getting `NativeArray` of UnitMoverData from entityQuery


```csharp 
NativeArray<Entity> entityArray = entityQuery.ToEntityArray(Allocator.Temp);;
NativeArray<UnitMoverData> unitMoverArray = entityQuery.ToComponentDataArray<UnitMoverData>(Allocator.Temp);;
```

### Updating Query using CopyFromComponentDataArray

`CopyFromComponentDataArray` - updates **Query**(`EntityQuery`) with modified `NativeArray` of component data.

>❗️This is the only way to update component data in `EntityQuery` from `MonoBehaviour` script. Instead of updateing each entity one by one using `EntityManager.SetComponentData` in a loop.


```csharp
for (int i = 0; i < unitMoverArray.Length; i++)
{
     var unitMover = unitMoverArray[i];
     unitMover.TargetPosition = mouseWorldPosition;
     unitMoverArray[i] = unitMover;
    //entityManager.SetComponentData(entityArray[i], unitMover); // ❌ Not allowed in MonoBehaviour
}
// Update the entities with the modified component data
entityQuery.CopyFromComponentDataArray(unitMoverArray);
```

