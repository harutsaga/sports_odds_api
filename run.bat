python manage.py makemigrations
if errorlevel 1 ( 
   echo makemigrations failed
) else (
    python manage.py migrate
    if errorlevel 1 (
        echo migrate failed
    ) else (
        python manage.py runserver 0.0.0.0:8000
    )
)