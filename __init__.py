bl_info = {
    "name": "Add Blender de Corte (Irregular Joint)",
    "author": "maikon177 + Grok",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Corte",
    "description": "Cria encaixes irregulares com tolerância para impressão em resina",
    "category": "3D Printing",
}

import bpy
import bmesh
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
    PointerProperty,
)
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup,
)


# ------------------------------------------------------------
# Properties (Configurações)
# ------------------------------------------------------------

class CorteProperties(PropertyGroup):

    max_polygons: IntProperty(
        name="Máx. Polígonos",
        description="Quantidade máxima de polígonos por objeto antes de fazer Decimate",
        default=500000,
        min=50000,
        max=2000000,
    )

    merge_distance: FloatProperty(
        name="Merge Distance",
        description="Distância para juntar vértices duplicados",
        default=0.0001,
        min=0.0,
        precision=5,
    )

    draft_angle: FloatProperty(
        name="Draft Angle",
        description="Ângulo de saída em graus (1° a 3° recomendado)",
        default=1.5,
        min=0.0,
        max=10.0,
        precision=1,
    )

    main_tolerance: FloatProperty(
        name="Tolerância Principal (mm)",
        description="Folga do encaixe principal (recomendado 0.15 ~ 0.25 para resina)",
        default=0.20,
        min=0.05,
        max=1.0,
        precision=2,
    )

    magnet_tolerance: FloatProperty(
        name="Tolerância Ímã (mm)",
        description="Folga do furo do ímã",
        default=0.10,
        min=0.02,
        max=0.5,
        precision=2,
    )


# ------------------------------------------------------------
# Operator: Preparar Objetos
# ------------------------------------------------------------

class CORTE_OT_preparar_objetos(Operator):
    bl_idname = "corte.preparar_objetos"
    bl_label = "Preparar Objetos"
    bl_description = "Aplica Scale/Rotation, modificadores, limpa normals e prepara os objetos"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.corte_props
        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if len(selected) == 0:
            self.report({'ERROR'}, "Nenhum objeto Mesh selecionado")
            return {'CANCELLED'}

        total_steps = 6
        wm = context.window_manager
        wm.progress_begin(0, total_steps)

        try:
            # ---- 1/6 Scale + Rotation ----
            wm.progress_update(1)
            self.report({'INFO'}, "1/6 - Aplicando Scale e Rotation...")

            for obj in selected:
                context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            # ---- 2/6 Aplicar Modificadores ----
            wm.progress_update(2)
            self.report({'INFO'}, "2/6 - Aplicando modificadores...")

            for obj in selected:
                context.view_layer.objects.active = obj
                # Aplica do último para o primeiro para evitar problemas de ordem
                for mod in reversed(obj.modifiers):
                    try:
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                    except Exception:
                        # Alguns modificadores podem falhar (ex: se dependem de outro objeto)
                        self.report({'WARNING'}, f"Não foi possível aplicar o modificador {mod.name} em {obj.name}")

            # ---- 3/6 Verificar polígonos + Decimate ----
            wm.progress_update(3)
            self.report({'INFO'}, "3/6 - Verificando quantidade de polígonos...")

            for obj in selected:
                mesh = obj.data
                face_count = len(mesh.polygons)

                if face_count > props.max_polygons:
                    self.report({'WARNING'}, f"{obj.name} tem {face_count} faces. Aplicando Decimate...")

                    context.view_layer.objects.active = obj
                    mod = obj.modifiers.new(name="Decimate_Corte", type='DECIMATE')
                    mod.ratio = props.max_polygons / face_count
                    bpy.ops.object.modifier_apply(modifier=mod.name)

            # ---- 4/6 Recalculate Outside ----
            wm.progress_update(4)
            self.report({'INFO'}, "4/6 - Corrigindo Normals...")

            for obj in selected:
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')

            # ---- 5/6 Merge by Distance ----
            wm.progress_update(5)
            self.report({'INFO'}, "5/6 - Limpando vértices duplicados...")

            for obj in selected:
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=props.merge_distance)
                bpy.ops.object.mode_set(mode='OBJECT')

            # ---- 6/6 Verificação Manifold (básica) ----
            wm.progress_update(6)
            self.report({'INFO'}, "6/6 - Verificando Manifold...")

            for obj in selected:
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                bm.edges.ensure_lookup_table()

                non_manifold = [e for e in bm.edges if not e.is_manifold]

                if non_manifold:
                    self.report({'WARNING'}, f"{obj.name} ainda tem {len(non_manifold)} arestas non-manifold")
                else:
                    self.report({'INFO'}, f"{obj.name} parece manifold")

                bm.free()

            self.report({'INFO'}, "Preparação concluída!")

        except Exception as e:
            self.report({'ERROR'}, f"Erro durante a preparação: {str(e)}")
            wm.progress_end()
            return {'CANCELLED'}

        wm.progress_end()
        return {'FINISHED'}


# ------------------------------------------------------------
# Panel
# ------------------------------------------------------------

class CORTE_PT_main_panel(Panel):
    bl_label = "Corte Irregular"
    bl_idname = "CORTE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Corte"

    def draw(self, context):
        layout = self.layout
        props = context.scene.corte_props

        # --- Botão principal de preparação ---
        box = layout.box()
        box.label(text="1. Preparação", icon='TOOL_SETTINGS')
        box.operator("corte.preparar_objetos", icon='CHECKMARK')

        layout.separator()

        # --- Configurações (Engrenagem) ---
        box = layout.box()
        box.label(text="Configurações", icon='PREFERENCES')

        col = box.column(align=True)
        col.prop(props, "max_polygons")
        col.prop(props, "merge_distance")
        col.prop(props, "draft_angle")

        layout.separator()

        col = box.column(align=True)
        col.prop(props, "main_tolerance")
        col.prop(props, "magnet_tolerance")

        layout.separator()

        # --- Área futura ---
        box = layout.box()
        box.label(text="2. Encaixe (em breve)", icon='MOD_BOOLEAN')
        box.label(text="• Escolher Macho / Fêmea")
        box.label(text="• Profundidade de inserção")
        box.label(text="• Pinos e Ímãs")


# ------------------------------------------------------------
# Registro
# ------------------------------------------------------------

classes = (
    CorteProperties,
    CORTE_OT_preparar_objetos,
    CORTE_PT_main_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.corte_props = PointerProperty(type=CorteProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.corte_props


if __name__ == "__main__":
    register()
