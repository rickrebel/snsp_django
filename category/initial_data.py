from category.models import (
    StatusControl, PlaceType, Topic,
    PriorityGroup, AgentType
)


class InitStatusControl:
    def __init__(self):
        initial_data = [
            (
                'pending',  # name (PK)
                'goal',  # group
                'Pendiente',  # public_name
                'Aún no se realizan actividades para atender al objetivo',
                '#FFC107',  # color
                'hourglass',  # icon
                1,  # order
                False,  # is_final
                0,  # priority
            ),
            (
                'in_progress',
                'goal',
                'En proceso',
                'Ya se comenzaron las actividades para atender al objetivo',
                '#003C71',
                'clock_loader_40',
                2,
                False,
                0,
            ),
            (
                'done',
                'goal',
                'Objetivo cumplido',
                'El objetivo fue abordado satisfactoriamente',
                '#28A745',
                'check',
                3,
                True,
                0,
            ),
            (
                'not_addressed',
                'goal',
                'No abordado',
                'El objetivo no se abordó',
                '#DC3545',
                'x',
                4,
                True,
                0,
            ),
            (
                'canceled',
                'goal',
                'Cancelado',
                'El objetivo fue cancelado',
                '#6C757D',
                'ban',
                5,
                True,
                0,
            ),
        ]

        for name, group, public_name, description, color, icon, order, is_final, priority in initial_data:
            StatusControl.objects.update_or_create(
                name=name,
                defaults={
                    'group': group,
                    'public_name': public_name,
                    'description': description,
                    'color': color,
                    'icon': icon,
                    'order': order,
                    'is_final': is_final,
                    'priority': priority,
                }
            )

        print('✓ Status Control created/updated')


class InitStatus:
    def __init__(self):
        init_status = [
            # is_public, open_editor, is_deleted
            ("draft", "register", "Borrador",
                "blue", "edit_note", False, None, False, 8),
            ("created", "register", "Enviado (para revisarse)",
                "green", "pending_actions", True, None, False, 6),
            ("need_changes", "register", "Requiere cambios",
                "orange", "new_releases", False, None, False, 2),
            ("need_new_checking", "register", "Requiere nueva revisión",
                "pink", "report_gmailerrorred", False, None, False, 4),
            ("approved", "register", "Aprobado",
                "green", "done_all", True, None, False, 16),
            ("discarded", "register", "Descartado",
                "red", "heart_broken", True, None, False, 10),

            # ("sent_to_validation", "sending", "Enviado a validación",
            #     "green", "send", False, False, False, 22),
            # ("validation_in_process", "validation", "Validación en proceso",
            #     "blue", "hourglass_top", False, False, False, 42),
            # ("validated", "validation", "Validado",
            #     "green", "how_to_reg", True, False, False, 44),
        ]
        order = -1
        for data in init_status:
            # name, group, public_name, color, icon, is_public,
            # open_editor, is_deleted = data
            name = data[0]
            group = data[1]
            public_name = data[2]
            color = data[3]
            icon = data[4]
            is_final = data[5]
            # open_editor = data[6]
            # role = data[6]
            # is_deleted = data[7]
            try:
                priority = data[8]
            except IndexError:
                priority = 99
            try:
                description = data[9]
            except IndexError:
                description = None
            status, _ = StatusControl.objects.get_or_create(
                name=name
            )
            status.group = group
            status.public_name = public_name
            status.color = color
            status.icon = icon
            status.is_final = is_final
            order += 2
            if group == "register" and order < 20:
                order = 20
            if group == "location" and order < 40:
                order = 40
            status.order = order
            # status.open_editor = open_editor
            # status.role = role
            # status.is_deleted = is_deleted
            status.priority = priority
            status.description = description
            status.save()



class InitPlaceTypes:
    def __init__(self):
        initial_data = [
            ('Localidad', True, None),
            ('Escuela', False, None),
            ('Trabajo', False, None),
            ('Oficina de Gobierno', False, None),
            ('Albergue', False, None),
            ('Centro Comunitario', False, None),
            ('Centro de Adaptación social', False, None),
        ]

        for name, is_default, icon in initial_data:
            PlaceType.objects.update_or_create(
                name=name,
                defaults={
                    'is_default': is_default,
                    'icon': icon,
                }
            )

        print('✓ Place Types created/updated')


class InitTopics:
    def __init__(self):
        initial_data = [
            ('Saneamiento', 'recycling', '#E74C3C', False),
            ('Detección /Tamizaje', 'straighten', '#3498DB', False),
            ('Insumo /Medicamento', 'pill', '#9B59B6', False),
            ('Programa de Acción Específico', 'assignment_globe', '#1ABC9C', False),
            ('Servicios Urbanos', 'stethoscope', '#F39C12', False),
            ('Atención en Salud', 'syringe', '#16A085', False),
            ('Otra temática', 'circle', '#27AE60', True),
        ]

        for name, icon, color, is_other in initial_data:
            Topic.objects.update_or_create(
                name=name,
                defaults={
                    'icon': icon,
                    'color': color,
                    'is_other': is_other,
                }
            )

        print('✓ Topics created/updated')


class InitAgentTypes:
    def __init__(self):
        initial_data = [
            (
                'Guardián Comunitario',
                'Guardián',
                False,
                'Persona de la comunidad que realiza alguna actividad relacionada con la salud pública',
                '#3498DB',
                'person_heart',
            ),
            (
                'Líder Comunitario',
                'Líder',
                True,
                'Persona de la comunidad que tiene algún liderazgo distinto a la salud pública',
                '#27a673',
                'contact_emergency',
            ),
            (
                'Representante Institucional',
                'Repr. Instit.',
                True,
                'Representa a una institución',
                '#7b3ce7',
                'assured_workload',
            ),
        ]

        for name, short_name, need_institution, description, color, icon in initial_data:
            AgentType.objects.update_or_create(
                name=name,
                defaults={
                    'short_name': short_name,
                    'need_institution': need_institution,
                    'description': description,
                    'color': color,
                    'icon': icon,
                }
            )

        print('✓ Agent Types created/updated')


class InitPriorityGroups:
    def __init__(self):
        initial_data = [
            'Comunidad indigena',
            'Afrodescendiente',
            'LGBTIIIQ+',
            'Personas en situación de calle',
            'personas con alguna discapacidad',
        ]

        for name in initial_data:
            PriorityGroup.objects.update_or_create(
                name=name,
                defaults={ }
            )

        print('✓ Priority Groups created/updated')