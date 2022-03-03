import bpy;
from math import radians;
from bpy.props import *;

class IconSceneLoader(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.icon_scene_loader";
    bl_label = "Icon Scene Loader";
    bl_options = {'REGISTER', 'UNDO'};
        
    # Create Properties
    show_overlays : BoolProperty(
        name = "Show Overlay",
        description = "Show Screen Space Overlays",
        default = False
    );
    
    light_energy : FloatProperty(
        name = "Light Strength",
        description = "Strength of the light source",
        default = 265.1,
        min = 0.0,
        max = 600.0
    );
    
    render_resolution_x : IntProperty(
        name = "Resolution X",
        description = "Render screen resolution X",
        default = 1024,
        min = 0,
        max = 8192
    );
    
    render_resolution_y : IntProperty(
        name = "Resolution Y",
        description = "Render screen resolution Y",
        default = 1024,
        min = 0,
        max = 8192
    );

    def execute(self, context):
        # Add Camera & Setup scene settings
        bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(0, 0, 5), rotation=(0, 0, 0), scale=(1, 1, 1));
        bpy.context.object.data.type = 'ORTHO';

        # Add Lighting
        bpy.ops.object.light_add(type='AREA', align='WORLD', location=(1.3982, -3.7477, 2.3), rotation=(0, 1.09, -1.21371), scale=(1, 1, 1));
        light_one = bpy.context.object.data; #543.4; #self.light_energy * 2.05;
        light_one.energy = 543.4;
        light_one.color = (1, 0, 0.260296);
        light_one.size = 7.3;
        light_one.shape = 'DISK';

        bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-3.765, 1.3508, 2.3), rotation=(0, 1.09, -9.76925), scale=(1, 1, 1));
        light_two = bpy.context.object.data;
        light_two.energy = self.light_energy; #265.1;
        light_two.color = (1, 0.350111, 0.12645);
        light_two.size = 7.3;
        light_two.shape = 'DISK';

        bpy.ops.object.light_add(type='AREA', align='WORLD', location=(-1.9921, 3.4686, 2.3), rotation=(0, 1.09, -4.19106), scale=(1, 1, 1));
        light_three = bpy.context.object.data;
        light_three.energy = self.light_energy; #265.1;
        light_three.color = (0.635915, 0.769926, 1);
        light_three.size = 7.3;
        light_three.shape = 'DISK';

        bpy.ops.object.light_add(type='AREA', align='WORLD', location=(2.8558, 2.8008, 2.3), rotation=(0, 1.09, -5.50751), scale=(1, 1, 1));
        light_four = bpy.context.object.data;
        light_four.energy = self.light_energy; #265.1;
        light_four.color = (1, 0.350111, 0.12645);
        light_four.size = 7.3;
        light_four.shape = 'DISK';

        # Add Dummy Object
        bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.object.shade_smooth(); # Shade smooth

        # Render settings
        context = bpy.context;
        render = context.scene.render;
        view_settings = context.scene.view_settings;
        cycles = context.scene.cycles;
        space_data = context.space_data;

        space_data.overlay.show_overlays = self.show_overlays;
        space_data.show_gizmo = self.show_overlays;
        
        render.resolution_y = self.render_resolution_y;
        render.resolution_x = self.render_resolution_x;
        render.film_transparent = True;
        view_settings.view_transform = 'Filmic';
        view_settings.look = 'Medium High Contrast';

        #Cycles settings
        render.engine = 'CYCLES';
        cycles.feature_set = 'EXPERIMENTAL';
        cycles.device = 'GPU';
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(IconSceneLoader.bl_idname, text=IconSceneLoader.bl_label);

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(IconSceneLoader);
    bpy.types.VIEW3D_MT_object.append(menu_func);


def unregister():
    bpy.utils.unregister_class(IconSceneLoader);
    bpy.types.VIEW3D_MT_object.remove(menu_func);


if __name__ == "__main__":
    register();

    # test call
    bpy.ops.object.icon_scene_loader();
