from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy import TypeDecorator, String
import json
import uuid


class JsonValue(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


def generate_uuid():
    return str(uuid.uuid4())


def get_or_create(session, model, **kwargs):
    try:
        query = session.query(model).filter_by(**kwargs)
        instance = query.first()

        if instance:
            return instance

        else:
            try:
                params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
                instance = model(**params)
                session.add(instance)
                session.commit()
                return instance

            except IntegrityError as e:
                session.rollback()
                instance = query.one()
                return instance

    except Exception as e:
        raise e
