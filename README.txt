!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Outra opção é utilizar o comando 
"Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass" 
que habilita só para esta sessão do powershell
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


python manage.py makemigrations
python manage.py migrate
python manage.py runserver


Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m venv .davi_venv
.\.davi_venv\Scripts\Activate.ps1
python manage.py makemigrations
python manage.py migrate
python manage.py runserver