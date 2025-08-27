# 🎮 Unity Examples

A collection of useful Unity code snippets and implementation patterns. 


## 🗺️ Screen Position to World Position

Convert screen coordinates to world space coordinates using the camera.

```csharp
Vector2 unitScreenPosition = Camera.main.WorldToScreenPoint(unitLocalTransform.Position);
````
