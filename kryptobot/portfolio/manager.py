from sqlalchemy import distinct
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import datetime
from ..core import Core
from ..db.models import Portfolio, Strategy, Harvester, Result, Backtest
from ..db.utils import get_or_create
from ..workers.strategy.tasks import schedule_strategy
from ..workers.harvester.tasks import schedule_harvester
# from ..workers.catalyst.tasks import schedule_catalyst_strategy
# from ..workers.core.tasks import schedule_core_strategy
from ..workers.t2.tasks import schedule_t2_strategy

pd.options.mode.chained_assignment = None

SMALL_SIZE = 12
MEDIUM_SIZE = 16
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


# TODO: strategies and harvesters should both be lists or dicts
class Manager(Core):

    portfolio_name = 'default'
    portfolio = None

    def __init__(self, config=None):
        super().__init__(config)
        if 'portfolio' not in self.config:
            self.config['portfolio']['name'] = 'default'
        self._session = self.session()
        self.portfolio_name = self.config['portfolio']['name']
        self.portfolio = self.add_record(
            Portfolio,
            name=self.portfolio_name
        )

    def __del__(self):
        self._session.close()

    def add_record(self, model, **kwargs):
        return get_or_create(
            self._session,
            model,
            {},
            **kwargs
        )

    def run_harvester(self, params):
        if self.portfolio is not None:
            params['portfolio_id'] = self.portfolio.id
            harvester = self.add_record(
                Harvester,
                porfolio_id=self.portfolio.id,
                class_name=params['harvester'],
                params=params,
                status='active'
            )
            params['harvester_id'] = harvester.id
        params['config'] = self.config
        schedule_harvester.apply_async(
            None,
            {'params': params},
            task_id=harvester.celery_id
        )
        return {'harvester_id': harvester.id}

    def run_strategy(self, params):
        if self.portfolio is not None:
            params['portfolio_id'] = self.portfolio.id
            strategy = self.add_record(
                Strategy,
                porfolio_id=self.portfolio.id,
                type=params['type'],
                class_name=params['strategy'],
                params=params,
                status='active'
            )
            params['strategy_id'] = strategy.id
        params['config'] = self.config
        # if params['type'] == 'core':
        #     schedule_core_strategy.apply_async(
        #         None,
        #         {'params': params},
        #         task_id=strategy.celery_id
        #     )
        # elif params['type'] == 'catalyst':
        #     schedule_catalyst_strategy.apply_async(
        #         None,
        #         {'params': params},
        #         task_id=strategy.celery_id
        #     )
        if params['type'] == 't2':
            schedule_t2_strategy.apply_async(
                None,
                {'params': params},
                task_id=strategy.celery_id
            )
        else:
            schedule_strategy.apply_async(
                None,
                {'params': params},
                task_id=strategy.celery_id
            )
        return {
            'strategy_id': strategy.id,
            'celery_id': strategy.celery_id
        }

    # paused, exited, archived
    # exited will go back to the quote currency
    # archived will store for historical data reference
    def stop_strategy(self, id, status="paused"):
        strategy = self._session.query(Strategy).filter(
            Strategy.id == id).first()
        strategy.status = status
        self._session.add(strategy)
        self._session.commit()

    def get_strategy_run_keys(self, strategy_id, simulated=True):
        if simulated:
            Model = Backtest
        else:
            Model = Result
        results = self._session.query(Model.run_key).filter(Model.strategy_id == strategy_id).distinct().all()
        return [r.run_key for r in results]

    def get_results(self, run_key, simulated=True):
        if simulated:
            Model = Backtest
        else:
            Model = Result
        results = self._session.query(Model).filter(Model.run_key == run_key).all()
        final = []
        for r in results:
            r.data['timestamp'] = self.convert_timestamp_to_date(r.data['timestamp'])
            final.append(r.data)
        return pd.DataFrame(final)

    def show_candle_chart(self, run_key, simulated=True):
        results = self.get_results(run_key, simulated)
        ohlc_cols = ['timestamp', 'open', 'high', 'low', 'close']
        quotes = results[ohlc_cols]
        result_count = len(quotes)
        quotes['timestamp'] = pd.to_datetime(quotes['timestamp'])
        quotes.set_index('timestamp', inplace=True)
        fig, ax = plt.subplots()
        candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),
                                 quotes['open'], quotes['high'],
                                 quotes['low'], quotes['close']),
                         width=0.001)
        ax.xaxis_date()
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_minor_locator(mdates.HourLocator(interval=2))
        if result_count < 1001:
            ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
        ax.grid(color='k', which="major", linestyle='-', linewidth=0.3)
        ax.grid(color='k', which="minor", linestyle='-', linewidth=0.1)
        ax.set_ylabel('Price')
        ax.autoscale_view()
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.gcf().set_size_inches(20, 5)
        plt.show()

    def show_indicator_charts(self, run_key, simulated=True):
        results = self.get_results(run_key, simulated)
        excluded = ['open', 'high', 'low', 'close']
        ind_cols = [c for c in results.columns if c not in excluded]
        inds = results[ind_cols]
        inds = inds.dropna(axis='columns')
        inds['timestamp'] = pd.to_datetime(inds['timestamp'])
        timestamps = inds['timestamp']
        inds.set_index('timestamp', inplace=True)
        result_count = len(inds)

        col_count = len(inds.columns) + 10
        count = 0
        for key in inds:
            count = count + 1
            if(self.is_number(inds[[key]].iloc[0])):
                ax = plt.subplot(col_count, 1, count)
                inds[[key]].plot(ax=ax)
                ax.set_ylabel(key)
                ax.xaxis.set_major_locator(mdates.DayLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
                ax.xaxis.set_minor_locator(mdates.HourLocator(interval=2))
                if result_count < 1001:
                    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
                ax.grid(color='k', which="major", linestyle='-', linewidth=0.3)
                ax.grid(color='k', which="minor", linestyle='-', linewidth=0.1)
            else:
                data = inds[key].tolist()
                df = pd.DataFrame(data)
                df['timestamp'] = timestamps
                df.set_index('timestamp', inplace=True)
                ax = plt.subplot(col_count, 1, count)
                df.plot(ax=ax)
                ax.set_ylabel(key)
                ax.xaxis.set_major_locator(mdates.DayLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
                ax.xaxis.set_minor_locator(mdates.HourLocator(interval=2))
                if result_count < 1001:
                    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
                ax.grid(color='k', which="major", linestyle='-', linewidth=0.3)
                ax.grid(color='k', which="minor", linestyle='-', linewidth=0.1)

        plt.gcf().set_size_inches(20, 140)
        plt.show()

    def convert_timestamp_to_date(self, timestamp):
        value = datetime.datetime.fromtimestamp(float(str(timestamp)[:-3]))
        return value.strftime('%Y-%m-%d %H:%M:%S')

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        except TypeError:
            return False
