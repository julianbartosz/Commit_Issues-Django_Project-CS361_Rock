import os
import sys
from dotenv import load_dotenv


def main():

    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'djangoProject1', '.env')
    load_dotenv(dotenv_path)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
