# 🎮 Unity Examples

A collection of useful Unity code snippets and implementation patterns. 

## Table of Contents

1. [🗺️ Screen Position to World Position](#%EF%B8%8F-screen-position-to-world-position)

## 🗺️ Screen Position to World Position

Convert screen coordinates to world space coordinates using the camera.

```csharp
Vector2 unitScreenPosition = Camera.main.WorldToScreenPoint(unitLocalTransform.Position);
````
