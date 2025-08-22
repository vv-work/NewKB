# Unity Input System 

## Installation

1. Open the Unity Package Manager (Window > Package Manager).
2. Unity Registry > Input 
![[Pasted image 20250817124920.png]]

3. Project > Context > Create> Input Actions
 ![[Pasted image 20250817125058.png]]

4. Name the file (e.g., "PlayerInputActions").

5. Double-click the created file to open the Input Actions editor.
![[Pasted image 20250817130811.png]]

6. Add Action Maps (e.g., "Player", "UI") and define actions (e.g., "Move", "Jump") with their bindings.
![[Pasted image 20250817130917.png]]
7. Add a new action by clicking the "+" button, name it (e.g., "Move"), and set its type (e.g., "Value" for movement).
![[Pasted image 20250817131301.png]] 
8. Generate the C# class by clicking the "Generate C# Class" button in the top right corner of the Input Actions editor.
![[Pasted image 20250817131700.png]]


## Using witn DOTS 

```csharp
[UpdateInGroup(typeof(SimulationSystemGroup))]
[UpdateBefore(typeof(PlayerShootingSystem))] 
public partial class PlayerInputSystem : SystemBase 
{
    protected override void OnCreate()
    {
        // Ensure an InputState singleton exists
        EntityQuery q = GetEntityQuery(ComponentType.ReadOnly<InputState>());
        if (q.IsEmptyIgnoreFilter)
        {
            Entity e = EntityManager.CreateEntity(typeof(InputState));
            EntityManager.SetName(e, "InputStateSingleton");
            EntityManager.SetComponentData(e, new InputState { ShootTriggered = false });
        }
    }
    protected override void OnUpdate()
    {
        bool shoot = false; 
        shoot |= Mouse.current.leftButton.wasPressedThisFrame; 
        var input = SystemAPI.GetSingletonRW<InputState>();
        input.ValueRW.ShootTriggered = shoot;
    }

}

public struct InputState : IComponentData
{
    public bool ShootTriggered;
    public float2 MovementDirection;
}
public partial class PlayerInputSystem : SystemBase
{

    private PlayerInputActions playerInputActions;

    protected override void OnCreate(){
        _playerInputActions = new PlayerInputActions();
    }

    protected override void OnStartRunning(){
        _playerInputActions.Enable();
    }

    protected override void OnStopRunning(){
        _playerInputActions.Disable();
    }

}
pro

```


## Instead of old Input Manager

### Getting mouse position 

```csharp
// Old Input Manager
Input.mousePosition

// New Input System
using UnityEngine.InputSystem;

Mouse.current.position.ReadValue();
```

### Getting Mouse World Positon on the ground plane

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

public class MouseWorldPosition : MonoBehaviour
{
    public Vector3 GetPosition()
    {
        Ray mouseCameraRay =  Camera.main.ScreenPointToRay(Mouse.current.position.ReadValue());
        Plane plane = new Plane(Vector3.up, Vector3.zero);
        
        if (plane.Raycast(mouseCameraRay, out float enter))
            return mouseCameraRay.GetPoint(enter);
        
        return Vector3.zero; 
    }
}
```

