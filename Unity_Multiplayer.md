![[Pasted image 20250917060047.png]]
[Multiplayer official Documentation](https://docs.unity3d.com/Manual/multiplayer.html)
## Getting started with networking concepts

![[Getting started with networking concepts [kVt0I6zZsf0].jpg]] 


![[ClientServer.gif]]

![[Pasted image 20250917070041.png]]

![[Pasted image 20250917070702.png]]

**UDP Protocol**

In unity **NGO** use UDP protocol for networking. 

+-------------------+--------------------+------------------+-------------------+
| Transport Header  | NGO Message Type   | Payload Data     | Checksum/Meta     |
+-------------------+--------------------+------------------+-------------------+
| Connection ID,    | e.g. "NetworkVar"  | Position,        | Sequence numbers, |
| Channel, Seq #    | or "ServerRpc"     | Rotation, etc.   | Delivery type     |
+-------------------+--------------------+------------------+-------------------+


![[UDP.gif]]

### Network Synchronization 

![[Pasted image 20250917090454.png]]
Client sends **RPC** server executes them and send SyncData 

### RPC(Remote Procedural Calls)

![[Pasted image 20250917091746.png]]

```csharp
[RPC(SendTo.Server)]
public void PingRpc(int pingCount){}

[RPC(SendTo.NotServer)]
public void PongRpc(int pongCount,string message){}
```
> ❗️ Require to end in **Rpc** by naming convention 



### Server Authority
![[Pasted image 20250917091054.png]]
### Server authority
### NetworkBehaviour

A `NetworkBehaviour` is a special type of `MonoeBehaviour` that provides networking capabilities.

**Network-specific hooks:**

- `OnNetworkSpawn()`: Called when the object is *spawned* on the network.
- `OnNetworkDespawn()`: Called when the object is *despawned* from the network.

**Newtwork Context Properties:**

- `IsServer`, `IsClient`, `IsOwner`,`OwnerClientId`

- **Allowes to declere network variables:**
- **Let's define `RPC`'s **

#### Example of NetworkBehaviour

```csharp

using Unity.Netcode;
using UnityEngine;

public class NetworkPlayer: NetworkBehaviour
{
    public NetworkVariable<int> health = new NetworkVariable<int>(100);

    public override void OnNetworkSpawn()
    {
        if (IsServer)
            health.Value = 100;

        // Subscribe to health changes
        health.OnValueChanged += OnHealthChanged;
    }

    private void OnHealthChanged(int oldValue, int newValue)
    {
        Debug.Log($"Health changed from {oldValue} to {newValue}");
    }

    [ServerRpc]
    public void TakeDamageServerRpc(int damage)
    {
        if (IsServer)
        {
            health.Value -= damage;
            if (health.Value <= 0)
            {
                // Handle player death
                Debug.Log("Player has died.");
            }
        }
    }

    private void OnDestroy()
    {
        // Unsubscribe from health changes
        health.OnValueChanged -= OnHealthChanged;
    } 

}

```
