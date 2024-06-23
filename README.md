# kanban|Board

**Aplikace pro správu a vizualizaci projektů.**

Tento projekt je webová aplikace pro správu úkolů a projektů pomocí metodiky Kanban. Aplikace umožňuje uživatelům přidávat, upravovat a sledovat úkoly v různých fázích dokončení.
## Instalace


>> Pro instalaci není nutné žádné virtuální prostředí. Avšak v případně potřeby lze
>> místo instalace balíčků z `requirements.txt` do lokálního prostředí, vytvořit virtuální
>> prostředí ve složce `.venv`.
1. Naklonujte repozitář
```bash
git clone https://github.com/jelinekjakub/kanbanboard.git
cd kanbanboard
```
2. Vytvořte soubor `.env` a nainstalujte potřebné závislosti
```bash
cp .env.example .env
pip install -r requirements.txt
```
3. Vytvořte sobory databáze
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
4. (Volitelné) Pokud chcete otestovat chování s různými daty, můžete použít příkaz `seed_db`
>> ⚠︎ **Upozornění:** příkaz `seed_db` smaže všechna aktuální data v databázi.
```bash
# (volitné)
python manage.py seed_db
```
5. Spustťe
```bash
python manage.py run
```

6. Nyní stačí otevřít webový prohlížeč na asdrese `http://localhost:5000/`.


## Klíčové funkce
Aplikace nabízí intuitivní uživatelské rozhraní, kde mohou uživatelé spravovat své úkoly v různých sloupcích (To Do, In Progress, Done), upravovat a mazat úkoly, spolupracovat na projektech s více uživateli a využívat responzivní design optimalizovaný pro různá zařízení.
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