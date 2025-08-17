## Unity ECS Advanced Concepts

## 🔍 SystemAPI.Query in Unity ECS

SystemAPI.Query is used inside `SystemBase` or `ISystem` to iterate over entities that match specific component types and filters.

It’s a type-safe, Burst-friendly way to access components without manually writing `Entities.ForEach`.


---

Basic Usage

```csharp
foreach (var (transform, velocity) in 
         SystemAPI.Query<RefRW<LocalTransform>, RefRO<Velocity>>()) { }
```
---


📜 Common Component Access Modifiers

Modifier	    Meaning	Example

```csharp
RefRO<T>	        //read-only access to component T	
RefRW<T>	        //Read-write access to component T	
EnabledRefRO<T>	//Read-only access for enabled/disabled components	
EnabledRefRW<T>	//Read-write access for enabled/disabled components
```

---

⚙ Filtering Methods

1. ```WithAll<T>()```

Selects entities that have all of the listed components or tags.

```csharp
SystemAPI.Query<RefRO<Health>>()
         .WithAll<PlayerTag, AliveTag>();
```


---

2. .`WithAny<T>()`

Selects entities that have at least one of the listed components.

```csharp
SystemAPI.Query<RefRO<Health>>()
         .WithAny<ZombieTag, VampireTag>();
```


---

3. .`WithNone<T>()`

Excludes entities with specific components.

```csharp
SystemAPI.Query<RefRO<Health>>()
         .WithNone<DeadTag>();
```


---

4. .`WithEntityAccess()`

Gives you access to the entity ID in the loop.

```csharp
foreach ((var transform, var entity) in 
         SystemAPI.Query<RefRO<LocalTransform>>()
                  .WithAll<PlayerTag>()
                  .WithEntityAccess())
{
    // entity is the Entity struct
}
```


---

5. ```.WithDisabled<T>()```

Includes entities where component T is disabled.

```csharp
SystemAPI.Query<RefRW<AIState>>()
         .WithDisabled<AIEnabled>();
```


---

🛠 Special Cases

Getting a Single Component

```csharp
var playerHealth = SystemAPI.GetSingleton<Health>();

var ecb = SystemAPI.GetSingleton<BeginInitializationEntityCommandBufferSystem.Singleton>()
                   .CreateCommandBuffer(World.Unmanaged);
```


---

Accessing Lookups

Lookups allow random access to component data outside of direct queries.
```csharp
var transformLookup = SystemAPI.GetComponentLookup<LocalTransform>(isReadOnly: false);
```

---

🚀 Performance Tips
	•	Use `RefRO` unless you need to modify — this allows Burst optimizations.
	•	Chain filters to reduce the number of entities processed.
	•	Use `.WithEntityAccess()` only if you really need the entity ID.

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

