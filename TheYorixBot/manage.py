import os
import pathlib
import sys

__all__ = ()


def main():
    file_path = pathlib.Path(__file__).resolve()
    current_path = file_path.parent
    project_root = current_path.parent
    sys.path.append(project_root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TheYorixBot.TheYorixBot.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?",
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
