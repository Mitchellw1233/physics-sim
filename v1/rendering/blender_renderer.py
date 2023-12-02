import bpy

from v1.engine.component.component import Component
from v1.rendering.renderer import Renderer


class BlenderRenderer(Renderer):
    def setup(self, frame: dict[int, Component]):
        self._clear_scene()

        bpy.context.scene.unit_settings.system = 'METRIC'
        bpy.context.scene.unit_settings.system_rotation = 'RADIANS'
        bpy.context.scene.unit_settings.length_unit = 'KILOMETERS'
        bpy.context.scene.unit_settings.mass_unit = 'KILOGRAMS'
        bpy.context.scene.unit_settings.time_unit = 'SECONDS'
        bpy.context.scene.unit_settings.temperature_unit = 'KELVIN'
        bpy.context.scene.render.fps = 30

        for cid in frame:
            self.add_component(frame[cid])

    def render_frame(self, frame: dict[int, Component]):
        for cid in frame:
            c = frame[cid]
            obj = bpy.data.objects[c.name]
            obj.location = (c.position.x, c.position.y, c.position.z)
            obj.rotation_quaternion = (c.rotation.w, c.rotation.x, c.rotation.y, c.rotation.z)
            obj.dimensions = (c.size.x, c.size.y, c.size.z)

    def next_frame(self):
        bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def add_component(self, c: Component):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=c.size.x/2,
            location=(c.position.x, c.position.y, c.position.z),
        )
        obj = bpy.context.active_object
        obj.name = c.name
        obj.rotation_mode = 'QUATERNION'
        obj.dimensions = (c.size.x, c.size.y, c.size.z)

    def remove_component(self, c: Component):
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[c.name].select_set(True)
        bpy.ops.object.delete()

    @staticmethod
    def _clear_scene():
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()
