# Laravel Forum API Megabit

<p align="center"><a href="https://laravel.com" target="_blank"><img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="400"></a></p>

<p align="center">
<a href="https://travis-ci.org/laravel/framework"><img src="https://travis-ci.org/laravel/framework.svg" alt="Build Status"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/dt/laravel/framework" alt="Total Downloads"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/v/laravel/framework" alt="Latest Stable Version"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/l/laravel/framework" alt="License"></a>
</p>


## Installation

Use the package manager [composer](https://getcomposer.org/download/) to install **Laravel Forum API Megabit**. This project is using [PHP 7](https://www.php.net/downloads.php/).

```bash
composer install
```

## Usage
* Setup mysql database and its credentials in **.env** file, see **.env.example** for example configurations. You can use XAMPP or others. 

  **Note:** use **utf8_unicode_ci** for database collation.
  
* Migrate this project to new database. Also setup Laravel Passport. 
  ```bash
  php artisan migrate:fresh && php artisan passport:install
  ```
* Run development server locally.
  ```bash
  php artisan serve
  ```
* The API will run on [http://localhost:8000](http://localhost:8000)

* See **routes/api.php** to know which route you have to visit. You can test the API using [Postman](https://www.postman.com/).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.