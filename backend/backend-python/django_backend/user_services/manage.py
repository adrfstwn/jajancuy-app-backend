#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management.commands.runserver import Command as runserver
from dotenv import load_dotenv

load_dotenv()

runserver.default_port = os.getenv('RUN_PORT')

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_services.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(

        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
