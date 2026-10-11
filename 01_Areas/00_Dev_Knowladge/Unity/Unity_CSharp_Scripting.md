
## Awaitable 
[Documentation Reference](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Awaitable.html)

### Async Function 

Making method `async` allows the use of `await` keyword incide it.

```csharp
public async Task LoadPlayerDataAsync()
{
    string json = await GetPlayerJsonAsync();
    PlayerData playerData = JsonUtility.FromJson<PLayerData>(json);
    Debug.Log("✅ Player data loaded");
}
```
**Return Types:**

- `Task` -> for Async operations that do not return a value.
- `Task<T>` -> for Async operations that return a value of type `T`.
- `void` -> for event handlers 
> ❗️not recommended for general use

### Unity Awaitables 

Unity 6 introduces **awaitables** that wrap Unity operations. These are much cleaner then using `yield`

```csharp
await Awaitable.NexFrameAsync();
await Awaitable.FixedUpdateAsync();
await Awaitable.WaitForSecondAsync(2f);
await Awaitable.FromAsyncOperation(asyncOperation);

await Awaitable.BackgroundThreadAsync();
//doing some havy math 
float = 42f;
//Switing back to main thread
await Awaitable.MainThreadAsync();

await SceneManager.LoadSceneAsync("Game");//Loading scnee async

```

### Example 

```csharp
using System.Threading.Tasks;
using UnityEngine;

public class AsyncExample: MonoBehaviour
{
    private async void Start()
    {
        Debug.Log("Start Async Example");
        await Awaitable.SecondAsync(3f);
        await LoadPlayerDataAsync()
        Debug.Log("Async Example Finished");
    }
}
