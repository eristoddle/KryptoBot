import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .configure import load_config
from .db.models import Base
from .publishers.ticker import Ticker


class Bot:

    strategy = None

    def __init__(self, strategy, config=None):
        self.strategy = strategy
        self.config = load_config(config)
        self.create_engine()

    def create_engine(self):
        db = self.config['db']
        if db['engine'] == 'sqlite':
            db_fullpath = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                db['name'])
            self.engine = create_engine(
                'sqlite:///{}'.format(db_fullpath),
                connect_args={
                    'check_same_thread': False},
                echo=False)
        else:
            conn_str = db['engine'] + '://' + db['user'] + ':' + db['pass'] \
                + '@' + db['host'] + ':' + db['port'] + '/' + db['name']
            self.engine = create_engine(conn_str)
        self.session = sessionmaker(bind=self.engine)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def drop_tables(self):
        print('Dropping tables...')
        Base.metadata.drop_all(self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def reset_db(self):
        print('Resetting database...')
        self.drop_tables()
        self.create_tables()

    def start_strategy(self):
        # TODO: All these adds are stupid, fix it
        self.strategy.add_session(self.session)
        self.strategy.add_keys(self.config['apis'])
        self.strategy.add_ticker(Ticker)
        self.strategy.run_simulation()
        self.strategy.start()

    def start(self):
        try:
            self.create_tables()
            self.start_strategy()

        except Exception as e:
            print(e)

        finally:
            self.engine.dispose()

    @classmethod
    def create(self, data):
        Class = self
        self = Class()
        print 'My Blocking Stuff'
