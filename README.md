# physics-sim
Experimental simulation of physics bodies interacting with each other. **This repo is very much a work in progress**.

### A few simulations
#### 20 random earth-sized body positions
A short example of using physics-sim to simulate 20 Earth-sized bodies at random positions pulling on each other by gravity. Blender is used as rendering engine in this case.

Video (clickable):
[![video](https://img.youtube.com/vi/3ghCybJyddI/0.jpg)](https://youtu.be/3ghCybJyddI)


#### Earth orbiting the Sun
A short example of using physics-sim to simulate Earths orbit around the Sun with Blender as rendering engine. The white line is a motion tracker of Blender which is enabled to make it visually more clear.

Video (clickable):
[![video](https://img.youtube.com/vi/zpYKn-mN8Zc/0.jpg)](https://youtu.be/zpYKn-mN8Zc)


### Issues to address
- No collision detection, therefore bodies can overlap each other (and leads to bodies pulling more gravitational force than usual)
- Blender's `bpy` library is very slow by appending frames, searching for alternatives
- Storage is implemented, but not yet being used for rendering
- Rotational and fluid related physics are not yet implemented
- Components are not yet using meshes, so everything is a sphere
- Python is not optimal for performance, but convenient for rapid prototyping
