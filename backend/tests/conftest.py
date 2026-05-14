import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.core.database import Base
from app.main import app
from app.core.config import get_settings
from datetime import datetime, timedelta
import jwt

settings = get_settings()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    from app.core.database import get_db
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    from app.core.database import get_db
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_db):
    from app.models.models import User
    from app.core.security import get_password_hash
    
    user = User(
        user_id="test_user_001",
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        created_at=datetime.utcnow()
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    access_token = jwt.encode(
        {
            "sub": test_user.user_id,
            "username": test_user.username,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def mock_amazon_api():
    from unittest.mock import Mock
    
    mock_api = Mock()
    mock_api.get_campaigns.return_value = [
        {
            "campaignId": "camp_001",
            "name": "Test Campaign",
            "status": "ENABLED",
            "budget": {"amount": 100.0}
        }
    ]
    
    mock_api.get_keywords.return_value = [
        {
            "keywordId": "kw_001",
            "keywordText": "test keyword",
            "matchType": "broad",
            "bid": 0.75
        }
    ]
    
    return mock_api


@pytest.fixture
def mock_cache():
    from unittest.mock import Mock
    
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mock_cache.set.return_value = True
    mock_cache.delete.return_value = True
    
    return mock_cache
