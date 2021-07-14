import bpy

bl_info = {
    "name": "Align Viewports Views",
    "description": "Align several 3Dviews from the active one (under mouse)",
    "author": "1C0D",
    "version": (1, 0),
    "blender": (2, 91, 0),
    "location": "View3D",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Align"}


def align(self,context):   

    i=None    
    ref_viewport = context.region_data #active RegionView3D 
    for i,r3d in enumerate(self.R3d):    
        if self.collections[i].value:                           
            for attribute in self.attributes:
                setattr(r3d, attribute, getattr(ref_viewport, attribute))
        else:
            for j,attribute in enumerate(self.attributes):
                setattr(r3d, attribute, self.m[i][j])


class AlignViewsProperty(bpy.types.PropertyGroup):
    """A bpy.types.PropertyGroup descendant for bpy.props.CollectionProperty"""
    # it's not possible to set the name dynamically, so keept it empty
    value = bpy.props.BoolProperty(name="")

class ALIGN_OT_ViewportsViews(bpy.types.Operator):
    """align several 3Dview regions from the active one (under mouse)"""
    bl_idname = "align.viewports_views"
    bl_label = "align viewports views"
    bl_options = {'REGISTER', 'UNDO'}
    
    collections = bpy.props.CollectionProperty(type=AlignViewsProperty)

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'

    def draw(self, context):
        layout = self.layout

        # expose all properties in the collection to the user
        for i,collection in enumerate(self.collections):
            layout.prop(collection, 'value', text=str(i))


    def invoke(self, context, event):

        self.attributes=['view_matrix', 'view_distance', 'view_perspective', 
            'use_box_clip', 'use_clip_planes', 
            'is_perspective',
            'show_sync_view', 'clip_planes']
            
        self.m=[]
        self.R3d = []
        
        self.collections.clear()
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':                
                r3d = area.spaces.active.region_3d
                ref_viewport = context.region_data
                
                if r3d == ref_viewport:
                    continue
                
                self.R3d.append(r3d) 
                
                collectionItem = self.collections.add()
                collectionItem.value = True
                
                n = []

                for attribute in self.attributes:
                    if attribute in {'view_matrix'} :
                        n.append(getattr(r3d, attribute).copy()) 
                    else:                        
                        n.append(getattr(r3d, attribute))
                self.m.append(n)


        return self.execute(context) 
        
        
    def execute(self, context):
   
        align(self,context)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(AlignViewsProperty)
    bpy.utils.register_class(ALIGN_OT_ViewportsViews)


def unregister():
    bpy.utils.unregister_class(ALIGN_OT_ViewportsViews)
    bpy.utils.unregister_class(AlignViewsProperty)
