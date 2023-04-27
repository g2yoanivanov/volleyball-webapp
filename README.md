# volleyball-webapp
Web application for information about volleyball tournaments, matches, halls, referees, teams and players with option to buy tickets for the matches

## Installation
1. Install Python
* Go to the official [Python website](https://www.python.org/)
* Click on the "Downloads" tab and select the latest version of Python for your operating system.
* Download the installation file.
* Run the installation file and follow the prompts to complete the installation process.
* Verify that Python is installed correctly by opening a command prompt (Windows) or terminal (Mac/Linux) and entering the command "python". 
* If Python is installed correctly, you should see a Python prompt appear.

2. Clone the reposotiroty
```bash
git clone https://github.com/g2yoanivanov/volleyball-webapp
```

3. Create a virtual environment and then activate it
```bash
python -m venv env
```
```bash
env\Scripts\activate
```

4. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.
```bash
pip install django
pip install django-crispy-forms
pip install Pillow
pip install qrcode
```

## How to start the server
1. Get the database up to date:
```bash
python manage.py makemigrations
python manage.py migrate
```

2. Create superuser
```bash
python manage.py createsuper
```

3. Navigate to the project's location and in the CMD write:
```bash
python manage.py runserver
```
