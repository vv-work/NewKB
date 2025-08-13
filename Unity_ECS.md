# Unity ECS 

- [Code Monkey ECS RTS game](https://www.youtube.com/watch?v=1gSnTlUjs-s)

## Code monkey Tutorial notes

- [Code Monkey 1h ECS Extreme Performance](https://www.youtube.com/watch?v=4ZYn9sR3btg)


### Questions 

- [ ] `SystemAPI` 
- [ ] `SystemAPI.Query`
- [ ] `SystemAPI.Time.DelataTime`

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

