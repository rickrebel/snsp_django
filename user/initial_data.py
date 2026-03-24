from user.models import Role


class InitRoles:
    def __init__(self):
        initial_data = [
            (
                'Director General',
                '',
                True,  # can_edit
                True,  # is_admin
                False,  # full_editor
            ),
            (
                'Admin',
                '',
                True,
                True,
                False,
            ),
            (
                'Auxiliar de Salud',
                '',
                False,
                False,
                False,
            ),
            (
                'Técnicos de Atención Primaria en Salud (TAPS)',
                '',
                False,
                False,
                False,
            ),
            (
                'Promotor',
                '',
                False,
                False,
                False,
            ),
            (
                'Director de Área',
                '',
                True,
                True,
                False,
            ),
        ]

        for name, description, can_edit, is_admin in initial_data:
            Role.objects.update_or_create(
                name=name,
                defaults={
                    'description': description,
                    'can_edit': can_edit,
                    'is_admin': is_admin,
                }
            )

        print('✓ Roles created/updated')


class InitUsers:

    def __init__(self):
        from user.models import User
        from geo.models import State, HealthDistrict

        # Verificar que existan los datos necesarios
        first_state = State.objects.first()
        first_health_district = HealthDistrict.objects.first()
        admin_role = Role.objects.filter(name='Admin').first()
        normal_role = Role.objects.filter(name='Auxiliar de Salud').first()

        if not first_state or not first_health_district:
            print('⚠️ Skipping users: Load territorial data first (State, HealthDistrict)')
            return

        if not admin_role or not normal_role:
            print('⚠️ Skipping users: Roles not found. Run InitRoles first')
            return

        initial_data = [
            (
                'admin@example.com',  # email (username)
                'Admin',  # first_name
                'Usuario',  # last_name
                'Prueba',  # last_name2
                '',  # phone
                'devpw',  # password
                first_state.id,
                first_health_district.id,
                admin_role.id,
                True,  # is_active
            ),
            (
                'user@example.com',
                'Usuario',
                'Normal',
                'Test',
                '',
                'devpw',
                first_state.id,
                first_health_district.id,
                normal_role.id,
                True,
            ),
        ]

        for email, first_name, last_name, last_name2, phone, password, state_id, hd_id, role_id, is_active in initial_data:
            user, created = User.objects.update_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'last_name2': last_name2,
                    'phone': phone,
                    'state_id': state_id,
                    'health_district_id': hd_id,
                    'role_id': role_id,
                    'is_active': is_active,
                }
            )
            if created:
                user.set_password(password)
                user.save()

        print('✓ Users created/updated')