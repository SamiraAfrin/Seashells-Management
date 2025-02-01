import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.seashells import SeaShell, Base
from app.repository.seashells import (
    get_all_seashells,
    add_seashell,
    get_seashell,
    update_seashell,
    delete_seashell,
)
from app.app_testconfig import TEST_DATABASE_URL

# Create a test db
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture to set up and tear down the test database
@pytest.fixture
def db_session():
    """Creates a new database session for a test."""
    Base.metadata.drop_all(bind=engine)  # Clean schema
    Base.metadata.create_all(bind=engine)  # Create tables
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  # Drop tables after test


def test_add_seashell(db_session):
    seashell1 = SeaShell(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    # Call the function
    result = add_seashell(seashell=seashell1, db=db_session)

    # Assertions
    assert result.name == "seashell1"  # Validate the created seashell


def test_get_all_seashells(db_session):
    seashell1 = SeaShell(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    seashell2 = SeaShell(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell2",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-2.png",
    )

    db_session.add(seashell1)
    db_session.add(seashell2)
    db_session.commit()

    # Call the function
    results = get_all_seashells(db_session)

    # Assertions
    assert len(results) > 0
    assert isinstance(results, list)  # Check the type
    assert results[0].name == "seashell1"  # Validate first seashell by name
    assert results[1].name == "seashell2"  # Validate second seashell by name


def test_get_seashell(db_session):
    seashell1 = SeaShell(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    db_session.add(seashell1)
    db_session.commit()

    # Call the function
    result = get_seashell(seashell_id=seashell1.id, db=db_session)

    # Assertions
    assert result.name == "seashell1"  # Validate the seashell by name


def test_update_seashell(db_session):
    seashell1 = SeaShell(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    db_session.add(seashell1)
    db_session.commit()
    created_obj = get_seashell(seashell_id=seashell1.id, db=db_session)

    seashell1_new = SeaShell(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1-new",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    # Call the function
    result = update_seashell(
        seashell_obj=created_obj, updated_seashell=seashell1_new, db=db_session
    )

    # Assertions
    assert result.name == "seashell1-new"  # Validate the updated seashell


def test_delete_seashell(db_session):
    seashell1 = SeaShell(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    db_session.add(seashell1)
    db_session.commit()
    created_obj = get_seashell(seashell_id=seashell1.id, db=db_session)

    # Call the function
    removed_obj = delete_seashell(seashell_obj=created_obj, db=db_session)
    result = get_seashell(seashell_id=removed_obj.id, db=db_session)

    # Assertions
    assert removed_obj.name == "seashell1"  # Validate the created seashell
    assert result == None  # After remove, nothing found
