# Django Forum API Megabit

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ForumAPI_Megabit. This project is using [Python 3](https://www.python.org/download/releases/3.0/).

```bash
pip install -r requirements.txt
```

## Usage
* Migrate first allowing Django generate your database schema. 
  ```bash
  python manage.py makemigrations && python manage.py migrate
  ```
  _This project still using db.sqlite3 by default so you don't have to setup database server using XAMPP for example._
* Set your superuser credentials to manage the database in [Django Admin](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/)
  ```bash
  python manage.py createsuperuser
  ```
  Go to [http://localhost:8000/admin](http://localhost:8000/admin) to manage the database.
* Run development server locally.
  ```bash
  python manage.py runserver
  ```
* The API will run on [http://localhost:8000](http://localhost:8000)

* See all **urls.py** files to know which route you have to visit. This project is using [Django Rest Framework](https://www.django-rest-framework.org/) so you can browse through API intuitively. You can also test the API using [Postman](https://www.postman.com/).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.