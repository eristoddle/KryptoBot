from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy import TypeDecorator, String
import simplejson as json
import uuid


class JsonValue(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if isinstance(value, dict):
            value = sort_dict(value)
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


def generate_uuid():
    return str(uuid.uuid4())


# TODO: This is to not get false positive uniques
# Not sure about arrsys, order may matter there
# Also not covering other edge cases
# Mainly custom for strategy and harvester params uniqueness
def sort_dict(value):
    sorted = {}
    for k, v in value.items():
        if isinstance(v, dict):
            sorted[k] = sort_dict(v)
        else:
            sorted[k] = v
    return sorted


def get_or_create(session, model, defaults=None, **kwargs):
    try:
        query = session.query(model).filter_by(**kwargs)
        instance = query.first()

        if instance:
            return instance

        else:
            try:
                params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
                params.update(defaults)
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
