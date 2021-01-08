# project_infog2
## Zombie Survival Social Network
### A system to share resources between non-infected humans on a zombie apocalyptic scenario

## Prerequisites
```
Python3
Pip
Python virtualenv
Django
Django Rest Framework
```

for the next steps it is necessary that the virtual environment is active

## Installing

```
pip install -r requirements.txt
```
### To do database migrations:

```
python manage.py migrate
```
# Running the Rest API
To run the Rest API

```
docker-compose up
```
or
```
python manage.py runserver
```
or 

 Access in: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
 
 ### Built With
 [Django Rest Framework](https://www.django-rest-framework.org/)
 
 # REST API

The REST API to the ZSSN is described below.

## All API endpoints:

- GET: `/` - API root
- GET/POST: `/survivors` - List all survivors / Add survivors
- GET/PATCH: `/survivors/<id-survivor-1>/trade-items/<id-survivor-2>` - Trade items between non infected survivors

## How to use API endpoints

## List all survivors

#### Method:

- GET: `/survivors`

#### URL Example:

> [http://127.0.0.1:8000/survivors/](http://127.0.0.1:8000/survivors/)

 
 
## Add Survivors

#### Method:

- POST: `/survivors/`

#### URL Example

> [http://127.0.0.1:8000/survivors/](http://127.0.0.1:8000/survivors/)

#### Paramethers

|  Paramether   |                    Description                     |                 Type                  |
| :-----------: | :------------------------------------------------: | :-----------------------------------: |
|     name      |                   Survivor name                    |                string                 |
|      age      |                    Survivor age                    |                number                 |
|    gender     |                  Survivor gender                   |                string                 |
| last_location | Last location of survivor (latitude and longitude) | {latitude: string, longitude: string} |
|     items     |                 Items of survivor                  |                array of objects                 |
|     items__name     |                 Item name                  |                string                 |
|     items__points     |                 Item points                  |                number                 |
|     items__quantity     |                 Item quantity                  |                number                 |

 
 JSON example:

```json
 {
        "id": 6,
        "inventory": {
            "id": 6,
            "items": [
                {
                    "id": 6,
                    "name": "Water",
                    "points": 4,
                    "quantity": 2
                },
                {
                    "id": 7,
                    "name": "Food",
                    "points": 3,
                    "quantity": 0
                },
                {
                    "id": 8,
                    "name": "Medication",
                    "points": 2,
                    "quantity": 0
                },
                {
                    "id": 9,
                    "name": "Ammunition",
                    "points": 1,
                    "quantity": 0
                }
            ]
        },
        "name": "daniel",
        "age": 23,
        "gender": "male",
        "longitude": 131564.0,
        "latitude": 123123.0,
        "is_infected": false,
        "count_reports": 1
    },
```

### Trade items between non infected survivors

#### Method

- GET/PATCH: `/survivors/<id-survivor-1>/trade-items/<id-survivor-2>`
  - `<id-survivor-1> is the identifier of the survivor 1`
  - `<id-survivor-2> is the identifier of the survivor 2`

#### URL example:

> [http://127.0.0.1:8000/survivors/1/trade-items/3](http://127.0.0.1:8000/survivors/1/trade-items/3)

#### Paramethers

| Paramether |      Description       |  Type  |
| :--------: | :--------------------: | :----: |
|  id  | Survivor identifier  | number |
| survivor_1  | Survivor 1 | object |
| trade_item  | Trade item | object |
| survivor_2  | Survivor 2 | object |

JSON example:

```json
[
  {
    "id": 1,
    "survivor_1": {
      "trade_item": {
        "Water": 1,
        "Medication": 1
      }
    }
  },
  {
    "id": 3,
    "survivor_2": {
      "trade_item": {
        "Food": 1,
        "Ammunition": 3
      }
    }
  }
]
```
## Authors

- [**David Mesquita Freitas**](https://github.com/davidmesquita/)

 
 
 
 
 
 
 
 
