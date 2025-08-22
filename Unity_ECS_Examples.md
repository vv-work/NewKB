# Unity ECS Examples


## System of looking where we move 
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
