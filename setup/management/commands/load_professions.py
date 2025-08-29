"""
Django management command to load professions data.

Usage:
    python manage.py load_professions
"""

from django.core.management.base import BaseCommand
from setup.models import Profession


class Command(BaseCommand):
    help = 'Load professions data into the database'

    def handle(self, *args, **options):
        # Lista de profissões para carregar
        professions = [
            "ADMINISTRADOR",
            "ADVOGADO",
            "AGRICULTOR",
            "ARQUITETO",
            "ARTESÃO",
            "ASSISTENTE SOCIAL",
            "ATENDENTE",
            "AUXILIAR ADMINISTRATIVO", 
            "CARPINTEIRO",
            "COMERCIANTE",
            "CONTADOR",
            "COZINHEIRO",
            "DENTISTA",
            "ELETRICISTA",
            "ENFERMEIRO",
            "ENGENHEIRO",
            "FARMACÊUTICO",
            "FISIOTERAPEUTA",
            "MECÂNICO",
            "MÉDICO",
            "MOTORISTA",
            "PEDREIRO",
            "PROFESSOR",
            "PSICÓLOGO",
            "RECEPCIONISTA",
            "SECRETÁRIO",
            "TÉCNICO DE ENFERMAGEM",
            "VENDEDOR",
            "VIGILANTE",
            "ZELADOR"
        ]

        self.stdout.write("📋 LOADING PROFESSIONS")
        self.stdout.write("="*50)
        
        # Counters for statistics
        created_count = 0
        updated_count = 0
        error_count = 0
        
        # Iterate over each profession
        for profession_name in professions:
            try:
                # Clean the name
                name = profession_name.strip()
                
                if not name:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️  Empty profession name, skipping...")
                    )
                    continue
                
                # Check if the profession already exists (by name)
                profession, created = Profession.objects.get_or_create(
                    name=name,
                    defaults={
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Created: {name}")
                    )
                    created_count += 1
                else:
                    # Update existing profession to ensure it's active
                    if not profession.is_active:
                        profession.is_active = True
                        profession.save()
                        self.stdout.write(
                            self.style.SUCCESS(f"🔄 Updated (activated): {name}")
                        )
                        updated_count += 1
                    else:
                        self.stdout.write(f"ℹ️  Already exists: {name}")
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error processing '{profession_name}': {str(e)}")
                )
                error_count += 1
        
        # Final summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write("📊 LOAD SUMMARY")
        self.stdout.write("="*50)
        self.stdout.write(self.style.SUCCESS(f"✅ Created: {created_count}"))
        self.stdout.write(self.style.SUCCESS(f"🔄 Updated: {updated_count}"))
        
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f"❌ Errors: {error_count}"))
        
        self.stdout.write(f"📋 Total processed: {len(professions)}")
        
        if error_count == 0:
            self.stdout.write(
                self.style.SUCCESS("\n🎉 All professions loaded successfully!")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"\n⚠️  {error_count} errors occurred during loading")
            )
