# Seashells-Management

## Project Description
It is a seashell management app built using Python. CRUD operations are implemented following clean-architecture. Here, FastAPI, SQLalchemy, and SQLite is used for the execution of the app. 

## How to start
Follow the following steps to start the web application.
1. Clone the repository to your destination.
2. Use `pipenv` to install necessary packages and set up a virtual environment.
3. Run `source venv/bin/active` to activate the virtual environment
4. Run `python main.py` to start the server.
5. Run `pytest` to run the test cases

## API Documentation
1. POST 
- **Path:** http://127.0.0.1:7777/v1/seashell
- **Method:** POST
- **NOTE:** Only `description` is optional

- **Example Payload:** 

```json
{
  "name": "Seashell_1",
  "collection_at": "2025-01-30T15:00:00",
  "description": "This is collected from   cox'z bazar",
  "species": "snail",
  "image": "seashell.png"
}
```
- **Response**
```json
{
    "message": "Seashell created successfully",
    "data": {
        "id": 126,
        "created_at": "2025-02-01T13:07:03",
        "updated_at": "2025-02-01T13:07:03",
        "collected_at": "2025-01-30T15:00:00",
        "name": "Seashell_1",
        "species": "snail",
        "description": "This is collected from  cox'z bazar",
        "image_url": "static/images/seashell_images/seashell.png"
    }
}
```

2. PATCH
- **Path:** http://127.0.0.1:7777/v1/seashell/{seashell_id}
- **Method:** PATCH
- **NOTE:** Every input is optional
- **Example Payload:** 

```json
{
  "name": "Seashell_updated",
  "collection_at": "2025-01-30T15:00:00",
  "description": "This is collected from   cox'z bazar",
  "species": "snail",
  "image": "seashell.png"
}
```
- **Response**
```json
{
    "message": "Seashell updated successfully",
    "data": {
        "id": 127,
        "created_at": "2025-02-01T13:08:14",
        "updated_at": "2025-02-01T13:08:45",
        "collected_at": "2025-01-30T15:00:00",
        "name": "Seashell_updated",
        "species": "snail",
        "description": "This is collected from cox'z bazar",
        "image_url": "static/images/seashell_images/seashell.png"
    }
}
```

3. GET
- **Path:** http://127.0.0.1:7777/v1/seashell/{seashell_id}
- **Method:** GET
- **Response**
```json
{
    "message": "Seashell retrived successfully",
    "data": {
        "id": 127,
        "created_at": "2025-02-01T13:08:14",
        "updated_at": "2025-02-01T13:08:45",
        "collected_at": "2025-01-30T15:00:00",
        "name": "Seashell_updated",
        "species": "snail",
        "description": "This is collected from cox'z bazar",
        "image_url": "static/images/seashell_images/seashell.png"
    }
}
```

4. GET
- **Path:** http://127.0.0.1:7777/v1/seashell
- **Method:** GET
- **NOTE:** Pagination limit is 10
- **Response**
```json
{
    "message": "Seashells retrived successfully",
    "data": [
        {
            "id": 1,
            "created_at": "2025-02-01T00:54:51",
            "updated_at": "2025-02-01T10:18:23",
            "collected_at": "2024-02-01T14:30:45",
            "name": "Updated_Seashell",
            "species": "snail",
            "description": "seashell description",
            "image_url": "static/images/seashell_images/seashell.png"
        },
        {
            "id": 2,
            "created_at": "2025-02-01T09:40:19",
            "updated_at": "2025-02-01T09:40:19",
            "collected_at": "2024-02-01T14:30:45",
            "name": "Test Seashell",
            "species": "snail",
            "description": "Test seashell description",
            "image_url": "static/images/seashell_images/seashell.png"
        },
        {
            "id": 3,
            "created_at": "2025-02-01T09:56:07",
            "updated_at": "2025-02-01T09:56:07",
            "collected_at": "2024-02-01T14:30:45",
            "name": "Test Seashell",
            "species": "snail",
            "description": "Test seashell description",
            "image_url": "static/images/seashell_images/image.png"
        },
        ......
      
    ]
}
```

5. DELETE
- **Path:** http://127.0.0.1:7777/v1/seashell/{seashell_id}
- **Method:** DELETE
- **Response**
```json
{
    "message": "Seashell deleted successfully",
    "data": {
        "id": 127,
        "created_at": "2025-02-01T13:08:14",
        "updated_at": "2025-02-01T13:08:45",
        "collected_at": "2025-01-30T15:00:00",
        "name": "Seashell_updated",
        "species": "snail",
        "description": "This is collected from cox'z bazar",
        "image_url": "static/images/seashell_images/seashell.png"
    }
}
```
