#!/usr/bin/env python3
import os
import sys

def main():
    """Função principal para comandos administrativos do Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar Django. Está instalado e disponível no seu ambiente?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

