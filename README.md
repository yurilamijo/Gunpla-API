# Gunpla API
Project to improve my Python skills.<br>
API build with Flask-RESTfull.
Database build with sqlite3 and postgresql<br>
Launched in Heruko.

## Getting Started

Setup virual enviroment
```
pip install virtualenv

virtualenv venv

# Mac OS
source ./venv/bin/activate

# Windows
.\venv\Scripts\activate
```

Install packages
```
pip install -r requirements.txt
```

Run it
```
python app.py
```

## API calls
Gunpla
*   GET     http://127.0.0.1:5000/gunplas
*   GET     http://127.0.0.1:5000/gunpla/<name>
*   POST    http://127.0.0.1:5000/gunpla/<name>
*   PUT     http://127.0.0.1:5000/gunpla/<name>
*   DELETE  http://127.0.0.1:5000/gunpla/<name>

Serie
*   GET     http://127.0.0.1:5000/series
*   GET     http://127.0.0.1:5000/series/<name>
*   POST    http://127.0.0.1:5000/series/<name>
*   DELETE  http://127.0.0.1:5000/series/<name>

User
*   POST    http://127.0.0.1:5000/login
*   POST    http://127.0.0.1:5000/logout
*   POST    http://127.0.0.1:5000/refresh
*   POST    http://127.0.0.1:5000/register

## Built With
* [Pyton 3.7.3](https://www.python.org/) - Programming lanuage

### Python packages
*   autopep8 
*   Flask 
*   Flask-JWT 
*   Flask-RESTful 
*   Flask-SQLAlchemy 
*   PyJWT-Extended 
*   pylint 
*   SQLAlchemy 

### Tools
* Heruko
* Postman
* Cloudflare

## Authors

* **Yuri Lamijo** - *Developer* - [Yuri Lamijo](...)