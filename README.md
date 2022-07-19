# LMS

A school management system for Ghanaian second-cycle institutions.

## Language and Libraries

- Python 3.9
- Django 3

## Installation

Clone this repository and open it in an editor.

```bash
git clone https://github.com/dodziraynard/curie.git
```

```bash
cd curie/src

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
```

Install npm packages for preprocessing static files.

```bash
yarn
```

## Running

Run this command to spin up the django development server.

```bash
python manage.py runserver

```

Then run the commands below to run the static files preprocessors.

```bash
npm start

```
