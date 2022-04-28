#  Stock Price

I use stocks data as a test input

Live -> [https://stockprice-1257c.web.app/](https://stockprice-1257c.web.app/)

Backend live -> [https://stockpricebackend.herokuapp.com](https://stockpricebackend.herokuapp.com)

Backend Repo -> [https://github.com/ankit123gupta/stockpricebackend](https://github.com/ankit123gupta/stockpricebackend)

Frontend Repo -> [https://github.com/ankit123gupta/stockpricefrontend](https://github.com/ankit123gupta/stockpricefrontend)



## installation
```
1 Go to project directory 

2 pip install -r requirements.txt

3 python manage.py runserver

```
live server is runing at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


### API discription

1 For Signup
```
url -> /api/signup/
method -> POST
body -> { 'username': USERNAME , 'password' : PASSWORD }

response -> django token
```

2 For login
```
url -> /login/
method -> POST
body -> { 'username': USERNAME , 'password' : PASSWORD }

response -> django token
```

3 Upload CSV File
```
url -> /api/uploadcsv
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> POST
body -> CSV file

response -> CSV data which are add to DB
```

4 Upload CSV data in JSON form
```
url -> /api/uploadjson
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> POST
body -> CSV data in json form

response -> {"msg":"file upload successfully"}
```

5 Get All Data
```
url -> /api/filter
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> GET

resprnse -> array containg all data
```

6 Get Filtered Data
```
url -> /api/filter/?date__lte=2008-07-03&date__gte=2008-07-03&symbol=GAIL
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> GET

resprnse -> array containg requested data

```
date__lte => date less than equal to

date__gte => date greater than equal to

symbol => symbol use by NSE/BSE for any company



7 Delete Data
```
url -> /api/delete/deletedata/?date__lte=2008-07-03&date__gte=2008-07-03&symbol=GAIL
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> GET

resprnse -> filter fields (i.e. date__lte=2008-07-03&date__gte=2008-07-03&symbol=GAIL)
```

Note: url -> /api/delete/deletedata/ will delete all data

8 Show Result categorized by company
```
url -> /api/showcategorizeddata
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> GET

resprnse -> dictionary required data
```

9 Search API
```
url -> /api/search/?search=GAIL,CIPLA
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> GET

resprnse -> array containg requested data
```


10 Get List of all company name
```
url -> /api/showdata/companylist
headers : { 'Authorization' : 'Token TOKEN_VALUE'}
method -> GET

resprnse -> array containg requested data
```








