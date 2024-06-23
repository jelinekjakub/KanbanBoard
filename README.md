# kanban|Board

**Aplikace pro správu a vizualizaci projektů.**

## Instalace
```bash
mv .env.example .env
pip install -r requirements.txt

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

# (optional)
python manage.py seed_db

python manage.py run
```

### Vysvětlení
- `mv .env.example .env` vytvoření .env sobouru.
- `pip install -r requirements.txt` instalace potřebných balíčků
- `python manage.py db commands` vytvoření, inicializace databáze a vytvoření migračních souborů 
- `python manage.py seed_db` zaplnění databáze částečně náhodnými testovacími daty
> ⚠︎ **Upozornění:** příkaz `seed_db` smaže všechna aktuální data v databázi.



## Instalace (old)
Aplikace se spouští pomocí `python manage.py run` 

Před prvním spuštěním je však potřeba ještě pár kroků:  
1. Nainstalujte si potřebné balíčky `pip install -r requirements.txt`
2. Zkopírujte soubor `.env.example`, pojmenujte ho `.env` a upravte potřebné hodnoty jako třeba `DATABASE_URL`, podle vašeho prostředí.
3. Udělejte a spusťte migrace pomocí příkazů:   
        - `python manage.py db init`  
        - `python manage.py db migrate`  
        - `python manage.py db upgrade`  
4. Spusťte aplikaci pomocí `python manage.py run`  

## Klíčové funkce
### Uživatel
Přihlašovací systém, přihlašování a registrace nových uživatelů.
### Tým
Tvorba týmu, přidávání uživatelů, pozvánky a sdílení projektů
### Projekt
Tvorba projektů, vizualizace postupu, kanban tabule s drag and drop funkcí, deadline
### Úkol
Tvorba úkolů s deadline, statusy, vizualizace
### Statistika
Burndown chart a velocity

## Použité technologie
### Backend
- Flask https://flask.palletsprojects.com/
- SQLite https://www.sqlite.org/
### Frontend
- Jinja https://jinja.palletsprojects.com/
- Tailwind https://tailwindcss.com/
- Alpine.js https://alpinejs.dev/
- Heroicons https://heroicons.com/
- Chart.js https://www.chartjs.org/