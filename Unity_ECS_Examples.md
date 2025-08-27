# 🎮 Unity ECS Examples

This collection showcases practical Unity ECS implementation patterns and common use cases.


## 🧭 System for Looking Where We Move

This system demonstrates how to make entities look in the direction they are moving, combining movement and rotation logic. 
```csharp
        public void OnUpdate(ref SystemState state) {

            foreach (var (localTransform, moveSpeed) in
                     SystemAPI.Query<
                         RefRW<LocalTransform>, 
                         RefRO<MoveSpeedData>>()
                    )
            {
                var targetPosition = localTransform.ValueRO.Position + new float3(10, 0, 0);
                var moveDirection = targetPosition - localTransform.ValueRW.Position; 
                moveDirection = math.normalize(moveDirection);
                
                localTransform.ValueRW.Rotation = quaternion.LookRotation(moveDirection, math.up());
                localTransform.ValueRW.Position += moveDirection*SystemAPI.Time.DeltaTime * moveSpeed.ValueRO.Value;
                
            }
```
