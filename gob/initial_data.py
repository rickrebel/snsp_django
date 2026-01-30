from gob.models import Institution, Program, Action


class InitInstitutions:
    def __init__(self):
        initial_data = [
            ('SNSP', 'Servicio Nacional de Salud Pública', 1),
            ('DS / JS', 'Distrito de Salud', 2),
            ('IMSS', '', 3),
            ('IMSS-BIENESTAR', '', 4),
            ('ISSSTE', '', 5),
            ('participacion ciudadana ', 'ciudadanía', 6),
            ('Secretaría de la Defensa', 'SEDENA', 7),
            ('Secretaría de Marina', 'SEMAR', 8),
            ('Autoridad Municipal', 'MUNICIPIO', 9),
            ('DIF', '', 10),
            ('Secretaría de Bienestar', 'BIENESTAR', 11),
        ]

        for name, short_name, order in initial_data:
            Institution.objects.update_or_create(
                name=name,
                defaults={
                    'short_name': short_name if short_name else None,
                    'order': order,
                }
            )

        print('✓ Institutions created/updated')


class InitPrograms:
    def __init__(self):
        initial_data = [
            (
                '3 por mi salud',
                '',
                '',
                True,
                'counter_3',
            ),
            (
                'Programa Nacional para la Prevención de Suicidio',
                'PRONAPS',
                '',
                True,
                'shield_with_heart',
            ),
            (
                'Piensa, lleguemos A SALV0',
                'A Salv0',
                '',
                True,
                'no_crash',
            ),
            (
                'Fortalecimiento a vacunación',
                'Vacunación',
                '',
                True,
                'vaccines',
            ),
        ]

        for name, short_name, description, is_internal, icon in initial_data:
            Program.objects.update_or_create(
                name=name,
                defaults={
                    'short_name': short_name,
                    'description': description if description else None,
                    'is_internal': is_internal,
                    'icon': icon if icon else None,
                }
            )

        print('✓ Programs created/updated')


class InitActions:
    def __init__(self):
        Action.objects.update_or_create(
            name='Conferencia / Plática',
            defaults={
                'description': 'Actividad de sensibilización o capacitación en comunidad',
            }
        )

        print('✓ Default Action created/updated')