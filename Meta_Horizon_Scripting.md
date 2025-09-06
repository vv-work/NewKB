# Meta Horizon Scripting


## Links

- [Horizon Scripting API Reference](https://developers.meta.com/horizon-worlds/reference/2.0.0/?utm_source=social-yt&utm_medium=M4D&utm_campaign=organic&utm_content=ScriptingYourWorld)
- [ Meta World Creation Manual](https://developers.meta.com/horizon-worlds/learn/documentation/mhcp-program/community-tutorials/creator-manual)


## **API** types

- Core API
- UI API
- Input API
- Camera API
- NavMesh API
- Analytics API
- Preformance API
- Unit AssetBundle API
- World Streaming API

## Key Scripting Elements 

- **World:** Container for youre entire title
- **Entity:** Any object in the world
- **Component:** A piece of functionality that can be added to an `entity`
- **Player:** Controler for user attributes and actions 
- **Asset:** Any 3D model, texture, sound, or other resource used in the world


## Basic Scripting Concepts

### Props 

```ts
import {Color, Component, PropTypes} from 'horizon/core'

class ExampleComponent extends Component<typeof ExampleComponent> {
    static propsDefinition = {
        myProp: { type: hz.PropTypes.Entity },
        timeout: { type: hz.PropTypes.Number, default: 3.0 },
        name : {type : PropTypes.String},
        color : {type : PropTypes.Color, default: new Color(1, 0.5, 0)}
    };

      override start() {
        console.log(this.props.name, this.props.color.toString())
      }
    }
    Component.register(ExampleComponent)
```


The static `propsDefinition` object defines your properties. Each property needs:
  * A *key* that will become the property name in `this.props`
  * An *object* value containing:
    * `type`: *Required*. a value from [PropTypes](#proptypes) (note that not all kinds of `PropTypes` are useful in a `propsDefinition`; see the limitations below).
    * `default`: *Optional*. Initial value for the property in the Properties panel.

| `PropTypes` Value | Results In | Default Value | Notes |
|-----------|-----------|---|---|
| `Number`  | `number`  | `0` | - |
| `String`  | `string`  | `''` | - |
| `Boolean` | `boolean` | `false` | - |
| `Vec3`    | `Vec3`    | `(0, 0, 0)` | - |
| `Color`   | `Color`   | `(0, 0, 0)` Black | RGB values between 0 and 1. |
| `Entity`  | `Entity \| null` | `null` | Cannot specify default |
| `Quaternion` | `Quaternion` | `(0, 0, 0)` | Properties panel value is edited as [YXZ Euler angles](#euler-angles) |
| `Asset`   | `Asset \| null` | `null` | Cannot specify default |

### Compoennt lifecycle 

The lifecycle of a component consists of three main phases: **preparation**, **start**, and **teardown**.

1. **Preparation** - When components are created.
    * Component allocation occurs
    * Constructor executes
    * Property initializers run
    * `initializeUI()` executes 
    * `preStart()` executes

2. **Start** - After preparation:
    * `start()` executes
    * `receiveOwnership()` executes (only during ownership transfers)
    * Component becomes "active" (begins processing events and timers)

3. **Teardown** - When the editor stops, component 
    * `transferOwnership()` executes (only during ownership transfers)
    * Component is [disposed](#disposing-objects), meaning that `dispose()` executes and all callbacks registered with `registerDisposeOperation` run, except for the ones where the `DisposeOperationRegistration` was already canceled or ran
    * All [async timeouts and intervals] created with the component are canceled.
    * All event subscriptions created with the component are 

### Subscribing to events

```ts
class ExampleComponent extends hz.Component<typeof ExampleComponent> {

    override preStart() {
        this.connectCodeBlockEvent(this.entity, hz.codeBlockEvents.onGrabStart, (isRightHand,player) => {
            this.entity.visibile.set(false)
            this.entity.collidable.set(false)

        }
    }
}
```

### Type Casting


```ts
this.prop.vfx.as(hz.ParticleSystem).play();
```
