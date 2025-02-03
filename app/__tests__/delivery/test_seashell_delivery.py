from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.seashells import Base
from app.delivery.seashells import get_database as get_db
from app.app_testconfig import TEST_DATABASE_URL

# Create a test db engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = ( #ensure routes use test session instead of real db session
        override_get_db  # whenever a route calls get_db, use test session
    )

    client = TestClient(app)  # to create an isolate env for every test

    yield session, client

    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)  # Cleanup database
    app.dependency_overrides.clear()  # Clear dependency overrides


def create_image():
    # Create a blank white image
    width, height = 100, 100  # specify dimensions
    blank_image = Image.new("RGB", (width, height), color="white")

    # Save the image to a BytesIO object insted of a file to mock
    img_byte_arr = (
        BytesIO()
    )  # BytesIO object is a type of in-memory binary stream, acts like a file, stay is memory not in disk
    blank_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(
        0
    )  # Move the cursor back to the beginning of the BytesIO object, to read the uploaded properly

    return img_byte_arr


def test_add_seashell(db_session):
    _, client = db_session
    # Create mock image data
    image_data = create_image()

    # Test data to send in the request
    files = {"image": ("image.png", image_data, "image/png")}
    data = {
        "name": "Seashell",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }

    response = client.post("/v1/seashell/", data=data, files=files)

    # Check if the response is successful
    assert response.status_code == 201
    assert response.json()["message"] == "Seashell created successfully"
    assert "data" in response.json()


def test_invalid_add_seashell(db_session):
    _, client = db_session

    invalid_file_data = "fake content"
    files = {
        "image": ("image.pdf", invalid_file_data, "application/pdf")
    }  # MIME - file type is pdf
    data = {
        "name": "Seashell",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }

    response = client.post("/v1/seashell/", data=data, files=files)

    # Check if the response
    assert response.status_code == 400


def test_update_seashell(db_session):
    _, client = db_session
    # Create mock image data
    image_data = create_image()

    # Test data to send in the request
    files = {"image": ("image.png", image_data, "image/png")}
    data = {
        "name": "Seashell",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }

    result = client.post("/v1/seashell/", data=data, files=files)
    updated_data = {
        "name": "Updated_Seashell",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }
    id = result.json()["data"]["id"]
    url = f"/v1/seashell/{id}"

    response = client.patch(url, data=updated_data, files=None)

    # Check if the response is successful
    assert response.status_code == 200
    assert response.json()["message"] == "Seashell updated successfully"
    assert "data" in response.json()
    assert response.json()["data"]["name"] == "Updated_Seashell"


def test_invalid_update_seashell(db_session):
    _, client = db_session

    updated_data = {
        "name": "Updated_Seashell",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }
    url = f"/v1/seashell/1"

    response = client.patch(url, data=updated_data, files=None)

    # Check if the response
    assert response.status_code == 404


def test_get_seashell(db_session):
    _, client = db_session
    image_data = create_image()

    files = {"image": ("image.png", image_data, "image/png")}
    data = {
        "name": "Seashell_new",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }

    result = client.post("/v1/seashell/", data=data, files=files)

    id = result.json()["data"]["id"]
    url = f"/v1/seashell/{id}"

    response = client.get(url)

    # Check if the response is successful
    assert response.status_code == 200
    assert response.json()["message"] == "Seashell retrived successfully"
    assert "data" in response.json()
    assert response.json()["data"]["name"] == "Seashell_new"


def test_get_invalid_seashell(db_session):
    _, client = db_session
    url = f"/v1/seashell/{100}"

    response = client.get(url)

    # Check if the response is a 404 error
    assert response.status_code == 404


def test_get_all_seashell(db_session):
    _, client = db_session
    # Create mock image data

    image_data = create_image()

    files = {"image": ("image.png", image_data, "image/png")}
    data = {
        "name": "Seashell_new",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }

    _ = client.post("/v1/seashell/", data=data, files=files)

    response = client.get("/v1/seashell/")

    # Check if the response is successful
    assert response.status_code == 200
    assert response.json()["message"] == "Seashells retrived successfully"
    assert "data" in response.json()
    assert len(response.json()["data"]) == 1


def test_get_empty_seashell_list(db_session):
    _, client = db_session

    response = client.get("/v1/seashell/")

    # Check if the response is successful
    assert response.status_code == 200
    assert response.json()["message"] == "Seashells retrived successfully"
    assert "data" in response.json()
    assert len(response.json()["data"]) == 0


def test_delete_seashell(db_session):
    _, client = db_session
    # Create mock image data
    image_data = create_image()

    files = {"image": ("image.png", image_data, "image/png")}
    data = {
        "name": "Seashell_delete_later",
        "collected_at": "2024-02-01T14:30:45",
        "species": "snail",
        "description": "seashell description",
    }

    result = client.post("/v1/seashell/", data=data, files=files)

    id = result.json()["data"]["id"]
    url = f"/v1/seashell/{id}"

    response = client.delete(url)

    # Check if the response is successful
    assert response.status_code == 200
    assert response.json()["message"] == "Seashell deleted successfully"
    assert "data" in response.json()
    assert response.json()["data"]["name"] == "Seashell_delete_later"


def test_delete_invalid_seashell(db_session):
    _, client = db_session

    response = client.delete("v1/seashell/1")

    # Check if the response
    assert response.status_code == 404
