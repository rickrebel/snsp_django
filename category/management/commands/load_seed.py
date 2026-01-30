
from django.core.management.base import BaseCommand
from category.initial_data import (
    InitStatus,
    InitStatusControl, InitPlaceTypes, InitTopics,
    InitAgentTypes, InitPriorityGroups
)
from gob.initial_data import (
    InitInstitutions, InitPrograms
)
from user.initial_data import InitRoles, InitUsers


class Command(BaseCommand):
    help = "Carga los datos iniciales (seed) para las aplicaciones."

    def handle(self, *args, **kwargs):
        print('Starting seed...')
        print('')

        # Category app seeds
        print('--- Seeding Category data ---')
        InitStatus()
        InitStatusControl()
        InitPlaceTypes()
        InitTopics()
        InitAgentTypes()
        InitPriorityGroups()
        print('')

        # Gob app seeds
        print('--- Seeding Gob data ---')
        InitInstitutions()
        InitPrograms()
        print('')

        # User app seeds
        print('--- Seeding User data ---')
        InitRoles()
        InitUsers()  # Requiere datos territoriales (State, HealthDistrict)
        print('')

        print('✓ Seed completed successfully!')

