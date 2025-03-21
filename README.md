# FantasyCPBL2025
<br />

## 目前進度: 

- 用戶 User
- CPBL球員資料 CPBL_Player
- 聯盟 League

<br />

## [Django Documentation](https://app-generator.dev/docs/technologies/django.html)

- [Getting Started with Django](https://app-generator.dev/docs/technologies/django/index.html)
- [Django Cheatsheet](https://app-generator.dev/docs/technologies/django/cheatsheet.html)
- [Adding Custom Commands in Django](https://app-generator.dev/docs/technologies/django/custom-command.html)
- [Integrate React in Django](https://app-generator.dev/docs/technologies/django/integrate-react.html)

<br />

## [Deploy on Render](https://app-generator.dev/docs/deployment/render/index.html) (free plan)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

<br /> 

## Manual Build 

> Download/Clone the sources  

```bash
$ git clone https://github.com/nishinokm/FantasyCPBL2025.git
$ cd FantasyCPBL2025
```

<br />

> Install modules via `pyenv`  

```bash
# windows 
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
pyenv update
pyenv install 3.11.7
pyenv local 3.11.7
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

<br />

> `Set Up Database`

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> `Start the App`

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />





---
Starter built with [Django App Generator](https://app-generator.dev/tools/django-generator/) - Open-source service for developers and companies.
