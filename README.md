# Kanban board

## Spuštění
Aplikace se spouští pomocí `python manage.py run`  

Před prvním spuštěním je však potřeba ještě pár kroků:  
1. Nainstalujte si potřebné balíčky `pip install -r requirements.txt`
1. Zkopírujte soubor `.env.example`, pojmenujte ho `.env` a upravte potřebné hodnoty jako třeba `mysql://root:secret@localhost/db`, podle vašeho prostředí.
2. Udělejte a spusťte migrace pomocí příkazů:   
        - `python manage.py db init`  
        - `python manage.py db migrate`  
        - `python manage.py db upgrade`  
3. Spusťte aplikaci pomocí `python manage.py run`  
