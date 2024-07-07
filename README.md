# MovieCollection

## Setup

Clone the repository:

```sh
$ git clone https://github.com/Krushna64/MovieCollection.git
$ cd MovieCollection
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv venv
$ venv\Scripts\activate
```

Upgrade pip (Optional):

```sh
(venv)$ python -m pip install -U pip
```

Install dependencies:

```sh
(venv)$ pip install -r requirements.txt
```

Run migrations:
```sh
(venv)$ python manage.py makemigrations movies
(venv)$ python manage.py migrate
```

Create a superuser (for admin access):
```sh
(venv)$ python manage.py createsuperuser
```

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(venv)$ python manage.py test
```

## Run the server

```sh
(venv)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.
