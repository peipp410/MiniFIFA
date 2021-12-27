# MiniFIFA

This is the course project for BI506-Database Concepts in SJTU. It is written by Django.

## Usage

1. Install Python and MySQL.
2. Install requirements

```shell
pip install -r requirements.txt
```

3. Initialize

```shell
python manage.py migrate
```

4. Import data into database. The data can be found in `./data`  in `.csv` format.
5. Run

```shell
python manage.py runserver 8000
```

Then enter the URL in the browser: http://127.0.0.1:8000/. You can get more information in the Tutorial page. 
