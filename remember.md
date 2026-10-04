at final stage use env for all this
1. in setting.py in databases
    database_user : Data123
    

    Migrations order
    # Built-in apps first
    python manage.py migrate contenttypes
    python manage.py migrate auth
    python manage.py migrate admin
    python manage.py migrate sessions

    # Then your custom apps
    python manage.py migrate authentication
    python manage.py migrate rooms
    python manage.py migrate bookings

    # Finally any remaining
    python manage.py migrate

    # When making model changes:
    python manage.py makemigrations
    python manage.py showmigrations  # Check the plan
    python manage.py migrate --plan  # See what will happen
    python manage.py migrate         # Apply migrations

If issues persist, use this nuclear option:
bash
# Completely reset everything
python manage.py reset_db --noinput
python manage.py remove_stale_contenttypes
python manage.py makemigrations
python manage.py migrate

    # First, migrate the built-in apps
    python manage.py migrate contenttypes
    python manage.py migrate auth
    python manage.py migrate admin
    python manage.py migrate sessions

    # Now create and migrate your custom apps
    python manage.py makemigrations authentication
    python manage.py migrate authentication

    python manage.py makemigrations rooms
    python manage.py migrate rooms

    python manage.py makemigrations bookings
    python manage.py migrate bookings

    # Finally, migrate any remaining built-in apps
    python manage.py migrate