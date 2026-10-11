# ⚡ Performance Optimization

Optimization techniques for high-performance Unity ECS applications using Burst and Jobs.

## Table of Contents

1. [🚀 Burst Compilation](#-burst-compilation)
   - [👩‍💼 Job System](#-job-system)
2. [🗃️ Data Structures](#%EF%B8%8F-data-structures)
   - [📊 NativeArray](#-nativearray)
   - [📊 DynamicBuffer](#-dynamicbuffer)

## 🚀 Burst Compilation

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

### 👩‍💼 Job System

The Job System enables parallel processing of entities for maximum performance.

`IJobEntity` - is a job entity that automatically iterates over entities with specified components.

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


## 🗃️ Data Structures

### 📊 NativeArray

 `NativeArray<T>` - is a Burst-compatible array that provides safe memory management and parallel job access.

> ❌ Not tied to entities.

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
:> [!WARNING]

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

### 📊 DynamicBuffer

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
