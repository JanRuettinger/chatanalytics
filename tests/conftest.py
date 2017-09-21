from project.factory import create_app
from project.factory import db as _db
from testing.postgresql import Postgresql
import pytest
import os
from distutils import dir_util



@pytest.yield_fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(scope='session')
def testapp(app):
    return app.test_client()


# @pytest.yield_fixture(scope='session')
# def db(app):
#     _db.app = app
#     _db.create_all()

#     yield _db

#     _db.drop_all()


# @pytest.fixture(scope='function', autouse=True)
# def session(db):
#     connection = db.engine.connect()
#     transaction = connection.begin()

#     options = dict(bind=connection, binds={})
#     session_ = db.create_scoped_session(options=options)

#     db.session = session_

#     yield session_

#     transaction.rollback()
#     connection.close()
#     session_.remove()


@pytest.fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir
