from sqlalchemy import Column, Integer, Numeric, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import datetime
from .utils import JsonValue, generate_uuid

Base = declarative_base()


class Ohlcv(Base):
    __tablename__ = 'ohlcv'

    id = Column('id', Integer, primary_key=True)
    exchange = Column('exchange', String)
    pair = Column('pair', String)
    timestamp = Column('timestamp', DateTime)
    open = Column('open', Float)
    high = Column('high', Float)
    low = Column('low', Float)
    close = Column('close', Float)
    volume = Column('volume', Float)
    interval = Column('interval', String)
    timestamp_raw = Column('timestamp_raw', Numeric)
    pair_id = Column('pair_id', Integer, ForeignKey('trading_pairs.id'))


class TradingPair(Base):
    __tablename__ = 'trading_pairs'

    id = Column('id', Integer, primary_key=True)
    exchange = Column('exchange', String)
    base_currency = Column('base_currency', String)
    quote_currency = Column('quote_currency', String)
    interval = Column('interval', String)


class TradingOrder(Base):
    __tablename__ = 'trading_orders'

    order_id = Column('order_id', Integer, primary_key=True)
    strategy_id = Column('strategy_id', Integer)
    # strategy_id = Column('strategy_id', Integer, ForeignKey('strategies.id'))
    timestamp = Column('timestamp', DateTime, default=datetime.datetime.utcnow)
    exchange = Column('exchange', String)
    pair = Column('pair', String)
    position = Column('position', String)
    amount = Column('amount', Float)
    price = Column('price', Float)
    simulated = Column('simulated', String)


class Strategy(Base):
    __tablename__ = 'strategies'

    id = Column('id', Integer, primary_key=True)
    type = Column('type', String, default='default')
    porfolio_id = Column('porfolio_id', Integer, ForeignKey('portfolios.id'))
    harvester_id = Column('harvester_id', Integer, ForeignKey('harvesters.id'))
    class_name = Column('class_name', String)
    params = Column('params', JsonValue)
    status = Column('status', String)
    celery_id = Column('celery_id', UUID, unique=True, nullable=False, default=generate_uuid)


class Harvester(Base):
    __tablename__ = 'harvesters'

    id = Column('id', Integer, primary_key=True)
    porfolio_id = Column('porfolio_id', Integer, ForeignKey('portfolios.id'))
    class_name = Column('class_name', String)
    params = Column('params', JsonValue)
    status = Column('status', String)
    celery_id = Column('celery_id', UUID, unique=True, nullable=False, default=generate_uuid)


class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)


class Result(Base):
    __tablename__ = 'results'

    id = Column('id', Integer, primary_key=True)
    strategy_id = Column('strategy_id', Integer, ForeignKey('strategies.id'))
    run_key = Column('run_key', UUID, nullable=False)
    timestamp = Column('timestamp', DateTime, default=datetime.datetime.utcnow)
    data = Column('data', JsonValue)


class Backtest(Base):
    __tablename__ = 'backtest'

    id = Column('id', Integer, primary_key=True)
    strategy_id = Column('strategy_id', Integer, ForeignKey('strategies.id'))
    run_key = Column('run_key', UUID, nullable=False)
    timestamp = Column('timestamp', DateTime, default=datetime.datetime.utcnow)
    data = Column('data', JsonValue)
