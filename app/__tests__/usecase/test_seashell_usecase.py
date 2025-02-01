import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.seashells import Base
from app.schemas.seashells import CreateSeaShellReq, UpdateSeaShellReq
from app.usecase.seashells import (
    add_seashell,
    get_seashell,
    get_all_seashells,
    update_seashell,
    delete_seashell,
)
from app.app_testconfig import TEST_DATABASE_URL

# Create a test db engine
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
    seashell_data = CreateSeaShellReq(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    seashell = add_seashell(seashellreq=seashell_data, db=db_session)

    # Assertions to check
    assert seashell is not None
    assert seashell.name == "seashell1"  # Check the name


def test_get_seashell(db_session):
    seashell_data = CreateSeaShellReq(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    seashell = add_seashell(seashellreq=seashell_data, db=db_session)
    result = get_seashell(seashell_id=seashell.id, db=db_session)

    # Assertions to check
    assert result is not None
    assert result.name == "seashell1"  # Check the name


def test_get_all_seashell(db_session):
    seashell_data_1 = CreateSeaShellReq(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    seashell_data_2 = CreateSeaShellReq(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell2",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    _ = add_seashell(seashellreq=seashell_data_1, db=db_session)
    _ = add_seashell(seashellreq=seashell_data_2, db=db_session)

    results = get_all_seashells(db=db_session)

    # Assertions to check
    assert results is not None
    assert len(results) > 0
    assert results[0].name == "seashell1"  # Check the name
    assert results[1].name == "seashell2"  # Check the name


def test_update_seashell(db_session):
    seashell_data_1 = CreateSeaShellReq(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    seashell_1 = add_seashell(seashellreq=seashell_data_1, db=db_session)
    retrived_obj = get_seashell(seashell_id=seashell_1.id, db=db_session)

    seashell_data_2 = UpdateSeaShellReq(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="updated_seashell",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    result = update_seashell(
        seashell_obj=retrived_obj, updated_seashellreq=seashell_data_2, db=db_session
    )

    # Assertions to check
    assert result is not None
    assert result.name == "updated_seashell"  # Check the name


def test_delete_seashell(db_session):
    seashell_data_1 = CreateSeaShellReq(
        collected_at=datetime.strptime("2024-02-01T14:30:45", "%Y-%m-%dT%H:%M:%S"),
        name="seashell1",
        species="snails",
        description="collected from cox's bazar",
        image_url="static/images/seashell_images/seashell-1.png",
    )

    seashell_1 = add_seashell(seashellreq=seashell_data_1, db=db_session)
    retrived_obj = get_seashell(seashell_id=seashell_1.id, db=db_session)

    deleted_obj = delete_seashell(seashell_obj=retrived_obj, db=db_session)

    result = get_seashell(seashell_id=deleted_obj.id, db=db_session)

    # Assertions to check
    assert result is None
