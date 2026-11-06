#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odamiylik_mulki.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django ni o'rnatmagan bo'lishi mumkin. "
            "'pip install django' ni ishlatib ko'ring."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
