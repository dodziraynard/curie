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
To set setup the desktop app, run the following commands

```bash
branch into feat-desktop-app
cd desktop-app/react-app
```
Install the required dependencies.
```bash
npm i
```
Then start the dev server
```bash
npm start
```
Whiles the dev server is on, copy the URL and do the following:
```bash
cd desktop-app/electron-app
```
Install the dependencies
```bash
npm i
```
Now, paste the React dev server link in this location inside the main.js file.
``` bash
win.loadURL(' http://127.0.0.1:5173/')
```
Finally, run the command:
```bash
npm start
```

