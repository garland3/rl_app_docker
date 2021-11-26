import datetime
import decimal
from typing import Iterable
from app.database import crud
import os
from app.database.database import SessionLocal
from fastapi import Depends
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime, time


MAX_JOB_RUN_TIME_SECONDS = os.environ.get('MAX_JOB_RUN_TIME_SECONDS', 60*9)
CLEAR_THE_QUEUE_SECRET = os.environ.get(
    'CLEAR_THE_QUEUE_SECRET', "clearthequeuetigerclemson")
ALIVE_FILENAME = os.environ.get('ALIVE_FILENAME', 'alive.txt')
MAX_DEAD_TIME = os.environ.get('MAX_DEAD_TIME', 5*60)
DEBUGGING = False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_if_alive(db, my_current_job_id: int = None):
    """Check if the alive table entry exist.
    If it exists, see how long it has been since someone wrote to it.
    If it has been too long, then probalby something died.
    If dead, return False
    if alive, return True"""

    # if a recent job was submitted, then don't worry about it.
    # assume everything is running ok.
    # if my_current_job_id is not None:
    alive_time = crud.get_1st_Alive_Time(db)
    if alive_time == None:
        print("Alive tims is None. Assume dead")
        return False

    diff_time = datetime.now() - alive_time
    if diff_time.total_seconds() > MAX_DEAD_TIME:
        print("Alive time stamp is too old. Assume dead")
        return False

    # print("Alive time is ok. Assume alive. ")
    return True


def say_im_alive(db):
    # print("Saving I'm alive. ")
    crud.update_Alive_with_now(db)


def say_im_dead(db):
    print("Recording dead status. ")
    crud.remove_Alive(db)


def compute_position_in_queue(db, job_id):
    my_job = crud.get_job(db, job_id)
    job_being_worked_on = crud.get_job_being_worked_on(db)
    if job_being_worked_on == None:
        return 0

    diff = my_job.id - job_being_worked_on.id
    return diff


def encode_json(obj):
    # if Iterable.
    if hasattr(obj, '__iter__'):
        return json.dumps([dict(r) for r in obj], cls=AlchemyEncoder)
    else:
        # print(dict(obj))
        return json.dumps(obj, cls=AlchemyEncoder)


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    # this will fail on non-encodable values, like other classes
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def row_to_dict(obj):
    if isinstance(obj.__class__, DeclarativeMeta):
        # an SQLAlchemy class
        fields = {}
        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            data = obj.__getattribute__(field)
            try:
                # this will fail on non-encodable values, like other classes
                json.dumps(data)
                fields[field] = data
            except TypeError:
                fields[field] = None
        # a json-encodable dict
        return fields
    return None
