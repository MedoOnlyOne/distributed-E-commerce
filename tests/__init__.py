import os
import pytest
import tempfile

from app import app, create_all

@pytest.fixture
def client():
    db1_fd, db1_path = tempfile.mkstemp()
    db2_fd, db2_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db1_path}'
    app.config['SQLALCHEMY_BINDS'] = {
        'db2': f'sqlite:///{db2_path}',
    }
    with app.app_context():
        with app.test_request_context():
            with app.test_client() as client:
                create_all()
                yield client
    os.close(db1_fd)
    os.close(db2_fd)
    os.unlink(db1_path)
    os.unlink(db2_path)
