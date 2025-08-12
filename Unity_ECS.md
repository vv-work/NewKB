# Unity ECS 

- [Code Monkey ECS RTS game](https://www.youtube.com/watch?v=1gSnTlUjs-s)

## Tutorial notes

- [Code Monkey 1h ECS Extreme Performance](https://www.youtube.com/watch?v=4ZYn9sR3btg)

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

`Baker` is used to convert `MonoBehaviour` data into ECS components. 

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

#### RerRO vs RefRW

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

#### Questions 

- [ ] SystemAPI 
- [ ] SystemAPI.Query
- [ ] SystemAPI.Time.DelataTime
