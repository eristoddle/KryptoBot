from core.database import ohlcv_functions
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.exponential_moving_average import exponential_moving_average as ema
from core.database import database
from ta.indicator import Indicator

engine = database.engine
conn = engine.connect()

class VolumeChangeMonitor(Indicator):
    def __init__(self, market, interval):
        super(VolumeChangeMonitor, self).__init__(market, interval, 2)
        self.write_strategy_description_to_db()
        self.__previous_volume = 0
        self.close = None
        self.timestamp = None
        self.value = None

    def next_calculation(self):
        """get latest N candles from market, do calculation, write results to db"""
        self.do_calculation()
        self.write_ta_statistic_to_db()

    def do_calculation(self):
        new_volume = self.market.latest_candle[5]
        if self.__previous_volume is not 0:
            self.value = (new_volume - self.__previous_volume)/self.__previous_volume # calculate change in volume in percent (decimal format)
        self.__previous_volume = new_volume
        self.timestamp = self.market.latest_candle[0]
        self.close = self.market.latest_candle[4]

    def write_ta_statistic_to_db(self):
        """Inserts average into table"""
        with database.lock:
                ins = database.TAVolumeChange.insert().values(Pair=self.market.analysis_pair, Time=self.timestamp, Close=self.close, INTERVAL=self.periods, VALUE=self.value)
                conn.execute(ins)
                print('Wrote statistic to db...')

    def write_strategy_description_to_db(self):
        '''Add ID and description to TAIdentifier table'''
        with database.lock:
            ins = database.TAIdentifier.insert().values(TA_ID=1, Description='Keeps track of volume changes between each period')
            conn.execute(ins)