bl_info = {
    "name": "Add Blender de Corte (Irregular Joint)",
    "author": "maikon177 + Grok",
    "version": (0, 2, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Corte",
    "description": "Cria encaixes irregulares com tolerância para impressão em resina",
    "category": "3D Printing",
}

import bpy
import bmesh
from mathutils import Vector
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty,
    EnumProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup,
)


# ------------------------------------------------------------
# Properties
# ------------------------------------------------------------

class CorteProperties(PropertyGroup):

    # --- Configurações gerais ---
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
        name="Draft Angle (°)",
        description="Ângulo de saída em graus (1° a 3° recomendado)",
        default=1.5,
        min=0.0,
        max=10.0,
        precision=1,
    )

    main_tolerance: FloatProperty(
        name="Tolerância Principal (mm)",
        description="Folga do encaixe principal (0.15~0.25 recomendado para resina)",
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

    insertion_depth: FloatProperty(
        name="Profundidade de Inserção (mm)",
        description="Quanto o macho entra dentro da fêmea",
        default=5.0,
        min=0.5,
        max=50.0,
        precision=1,
    )

    # --- Referências dos objetos ---
    male_object: PointerProperty(
        name="Macho",
        description="Objeto que entra (ex: ombro)",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'MESH'
    )

    female_object: PointerProperty(
        name="Fêmea",
        description="Objeto que recebe (ex: blusa)",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'MESH'
    )

    # --- Opções ---
    auto_backup: BoolProperty(
        name="Backup Automático",
        description="Duplicar e esconder os originais antes de cortar",
        default=True,
    )

    ask_cleanup: BoolProperty(
        name="Perguntar limpeza após Boolean",
        description="Após o corte, perguntar se deseja limpar a topologia",
        default=True,
    )


# ------------------------------------------------------------
# Funções auxiliares
# ------------------------------------------------------------

def get_unit_scale(context):
    """Retorna o fator para converter mm para unidades da cena"""
    unit_settings = context.scene.unit_settings
    if unit_settings.system == 'METRIC':
        if unit_settings.length_unit == 'MILLIMETERS':
            return 0.001  # 1mm = 0.001m
        elif unit_settings.length_unit == 'CENTIMETERS':
            return 0.01
        else:  # METERS
            return 1.0
    return 1.0


def check_units_warning(context, operator):
    """Avisa se a cena não está em milímetros"""
    unit_settings = context.scene.unit_settings
    if unit_settings.system != 'METRIC' or unit_settings.length_unit != 'MILLIMETERS':
        operator.report({'WARNING'},
            "Atenção: A cena não está em Milímetros. "
            "Recomendado: Scene Properties → Units → Metric → Millimeters")
        return False
    return True


def ensure_object_mode(context):
    if context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')


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
        ensure_object_mode(context)

        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']

        if len(selected) == 0:
            self.report({'ERROR'}, "Nenhum objeto Mesh selecionado")
            return {'CANCELLED'}

        check_units_warning(context, self)

        total_steps = 6
        wm = context.window_manager
        wm.progress_begin(0, total_steps)

        try:
            # 1/6 Scale + Rotation
            wm.progress_update(1)
            self.report({'INFO'}, "1/6 - Aplicando Scale e Rotation...")
            for obj in selected:
                context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            # 2/6 Aplicar Modificadores
            wm.progress_update(2)
            self.report({'INFO'}, "2/6 - Aplicando modificadores...")
            for obj in selected:
                context.view_layer.objects.active = obj
                for mod in reversed(list(obj.modifiers)):
                    try:
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                    except Exception:
                        self.report({'WARNING'}, f"Não foi possível aplicar {mod.name} em {obj.name}")

            # 3/6 Polígonos + Decimate
            wm.progress_update(3)
            self.report({'INFO'}, "3/6 - Verificando polígonos...")
            for obj in selected:
                face_count = len(obj.data.polygons)
                if face_count > props.max_polygons:
                    self.report({'WARNING'}, f"{obj.name}: {face_count} faces → Decimate")
                    context.view_layer.objects.active = obj
                    mod = obj.modifiers.new(name="Decimate_Corte", type='DECIMATE')
                    mod.ratio = props.max_polygons / max(face_count, 1)
                    bpy.ops.object.modifier_apply(modifier=mod.name)

            # 4/6 Normals
            wm.progress_update(4)
            self.report({'INFO'}, "4/6 - Corrigindo Normals...")
            for obj in selected:
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')

            # 5/6 Merge by Distance
            wm.progress_update(5)
            self.report({'INFO'}, "5/6 - Limpando vértices...")
            for obj in selected:
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles(threshold=props.merge_distance)
                bpy.ops.object.mode_set(mode='OBJECT')

            # 6/6 Manifold check
            wm.progress_update(6)
            self.report({'INFO'}, "6/6 - Verificando Manifold...")
            for obj in selected:
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                non_manifold = [e for e in bm.edges if not e.is_manifold]
                if non_manifold:
                    self.report({'WARNING'}, f"{obj.name}: {len(non_manifold)} arestas non-manifold")
                else:
                    self.report({'INFO'}, f"{obj.name}: OK (manifold)")
                bm.free()

            self.report({'INFO'}, "Preparação concluída!")

        except Exception as e:
            self.report({'ERROR'}, f"Erro: {str(e)}")
            wm.progress_end()
            return {'CANCELLED'}

        wm.progress_end()
        return {'FINISHED'}


# ------------------------------------------------------------
# Operator: Definir Macho
# ------------------------------------------------------------

class CORTE_OT_set_male(Operator):
    bl_idname = "corte.set_male"
    bl_label = "Definir como Macho"
    bl_description = "Define o objeto ativo como Macho (peça que entra)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Selecione um objeto Mesh")
            return {'CANCELLED'}

        props = context.scene.corte_props
        props.male_object = obj
        self.report({'INFO'}, f"Macho definido: {obj.name}")
        return {'FINISHED'}


# ------------------------------------------------------------
# Operator: Definir Fêmea
# ------------------------------------------------------------

class CORTE_OT_set_female(Operator):
    bl_idname = "corte.set_female"
    bl_label = "Definir como Fêmea"
    bl_description = "Define o objeto ativo como Fêmea (peça que recebe)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Selecione um objeto Mesh")
            return {'CANCELLED'}

        props = context.scene.corte_props
        props.female_object = obj
        self.report({'INFO'}, f"Fêmea definida: {obj.name}")
        return {'FINISHED'}


# ------------------------------------------------------------
# Operator: Backup
# ------------------------------------------------------------

class CORTE_OT_backup(Operator):
    bl_idname = "corte.backup"
    bl_label = "Fazer Backup"
    bl_description = "Duplica e esconde os objetos Macho e Fêmea"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.corte_props
        ensure_object_mode(context)

        backed = []
        for obj, label in [(props.male_object, "Macho"), (props.female_object, "Fêmea")]:
            if obj:
                # Duplica
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()
                new_obj.name = f"{obj.name}_BACKUP"
                context.collection.objects.link(new_obj)
                new_obj.hide_set(True)
                new_obj.hide_render = True
                backed.append(new_obj.name)

        if not backed:
            self.report({'ERROR'}, "Nenhum objeto Macho/Fêmea definido")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Backup criado: {', '.join(backed)}")
        return {'FINISHED'}


# ------------------------------------------------------------
# Operator: Criar Encaixe (versão inicial com tolerância)
# ------------------------------------------------------------

class CORTE_OT_criar_encaixe(Operator):
    bl_idname = "corte.criar_encaixe"
    bl_label = "Criar Encaixe com Tolerância"
    bl_description = "Aplica Boolean com tolerância (expande na Fêmea)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.corte_props
        ensure_object_mode(context)

        male = props.male_object
        female = props.female_object

        # Validações
        if not male or not female:
            self.report({'ERROR'}, "Defina o Macho e a Fêmea primeiro")
            return {'CANCELLED'}

        if male == female:
            self.report({'ERROR'}, "Macho e Fêmea não podem ser o mesmo objeto")
            return {'CANCELLED'}

        if male.type != 'MESH' or female.type != 'MESH':
            self.report({'ERROR'}, "Macho e Fêmea precisam ser objetos Mesh")
            return {'CANCELLED'}

        check_units_warning(context, self)

        # Backup automático
        if props.auto_backup:
            bpy.ops.corte.backup()

        try:
            unit_scale = get_unit_scale(context)
            tolerance = props.main_tolerance * unit_scale  # converte mm → unidade da cena

            # --- Cria um cortador a partir do Macho ---
            # Duplica o macho para usar como cortador
            cutter = male.copy()
            cutter.data = male.data.copy()
            cutter.name = "Cutter_Temp"
            context.collection.objects.link(cutter)

            # Expande o cortador com Solidify (tolerância)
            # Offset positivo + thickness = aumenta o tamanho
            context.view_layer.objects.active = cutter
            mod = cutter.modifiers.new(name="Tolerance", type='SOLIDIFY')
            mod.thickness = tolerance * 2
            mod.offset = 1.0  # expande para fora
            mod.use_even_offset = True
            bpy.ops.object.modifier_apply(modifier=mod.name)

            # Boolean na Fêmea (Difference) → cria o furo maior
            context.view_layer.objects.active = female
            bool_mod = female.modifiers.new(name="Corte_Femea", type='BOOLEAN')
            bool_mod.operation = 'DIFFERENCE'
            bool_mod.solver = 'EXACT'
            bool_mod.object = cutter

            try:
                bpy.ops.object.modifier_apply(modifier=bool_mod.name)
            except Exception:
                # Fallback para Fast
                bool_mod.solver = 'FAST'
                bpy.ops.object.modifier_apply(modifier=bool_mod.name)
                self.report({'WARNING'}, "Solver Exact falhou, usou Fast")

            # Remove o cortador temporário
            bpy.data.objects.remove(cutter, do_unlink=True)

            # Renomeia para ficar claro
            if not male.name.endswith("_Macho"):
                male.name = f"{male.name}_Macho"
            if not female.name.endswith("_Femea"):
                female.name = f"{female.name}_Femea"

            self.report({'INFO'}, f"Encaixe criado! Tolerância: {props.main_tolerance}mm na Fêmea")

            if props.ask_cleanup:
                self.report({'INFO'}, "Dica: Você pode limpar a topologia manualmente na região do corte se necessário.")

        except Exception as e:
            self.report({'ERROR'}, f"Erro ao criar encaixe: {str(e)}")
            return {'CANCELLED'}

        return {'FINISHED'}


# ------------------------------------------------------------
# Operator: Limpar referências
# ------------------------------------------------------------

class CORTE_OT_limpar_refs(Operator):
    bl_idname = "corte.limpar_refs"
    bl_label = "Limpar Macho/Fêmea"
    bl_description = "Remove as referências de Macho e Fêmea"

    def execute(self, context):
        props = context.scene.corte_props
        props.male_object = None
        props.female_object = None
        self.report({'INFO'}, "Referências limpas")
        return {'FINISHED'}


# ------------------------------------------------------------
# Panel Principal
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

        # ===== 1. PREPARAÇÃO =====
        box = layout.box()
        box.label(text="1. Preparação", icon='TOOL_SETTINGS')
        box.operator("corte.preparar_objetos", icon='CHECKMARK')

        # ===== 2. DEFINIR MACHO / FÊMEA =====
        box = layout.box()
        box.label(text="2. Definir Peças", icon='MOD_BOOLEAN')

        row = box.row(align=True)
        row.operator("corte.set_male", text="Definir Macho", icon='MESH_CUBE')
        row.operator("corte.set_female", text="Definir Fêmea", icon='MESH_ICOSPHERE')

        col = box.column(align=True)
        col.prop(props, "male_object", text="Macho")
        col.prop(props, "female_object", text="Fêmea")

        if props.male_object and props.female_object:
            if props.male_object == props.female_object:
                box.label(text="Erro: mesmo objeto!", icon='ERROR')
            else:
                box.label(text="Macho e Fêmea OK", icon='CHECKMARK')

        box.operator("corte.limpar_refs", text="Limpar seleção", icon='X')

        # ===== 3. ENCAIXE =====
        box = layout.box()
        box.label(text="3. Criar Encaixe", icon='MOD_SOLIDIFY')

        col = box.column(align=True)
        col.prop(props, "main_tolerance")
        col.prop(props, "insertion_depth")
        col.prop(props, "draft_angle")

        box.prop(props, "auto_backup")

        row = box.row()
        row.scale_y = 1.4
        row.operator("corte.criar_encaixe", icon='PLAY')

        # ===== 4. CONFIGURAÇÕES =====
        box = layout.box()
        box.label(text="Configurações", icon='PREFERENCES')

        col = box.column(align=True)
        col.prop(props, "max_polygons")
        col.prop(props, "merge_distance")
        col.prop(props, "magnet_tolerance")
        col.prop(props, "ask_cleanup")

        # ===== Ajuda rápida =====
        box = layout.box()
        box.label(text="Fluxo recomendado:", icon='INFO')
        box.label(text="1. Preparar Objetos")
        box.label(text="2. Definir Macho e Fêmea")
        box.label(text="3. Criar Encaixe")
        box.label(text="4. Testar impressão!")


# ------------------------------------------------------------
# Registro
# ------------------------------------------------------------

classes = (
    CorteProperties,
    CORTE_OT_preparar_objetos,
    CORTE_OT_set_male,
    CORTE_OT_set_female,
    CORTE_OT_backup,
    CORTE_OT_criar_encaixe,
    CORTE_OT_limpar_refs,
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
