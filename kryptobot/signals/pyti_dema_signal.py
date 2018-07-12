from ..signals.base_signal_generator import BaseSignalGenerator
from ..ta.pyti_exponential_moving_average import PytiEma


class PytiDemaSignal(BaseSignalGenerator):

    def __init__(self, market, interval, params, strategy):
        super().__init__(market, interval, strategy)
        short = params.pop('short_window', 12)
        long = params.pop('long_window', 26)
        self.last_signal = None
        self.repeat_count = 0
        self.repeat_limit = 0
        self.ema_short = PytiEma(
            market,
            interval,
            short
        )
        self.ema_long = PytiEma(
            market,
            interval,
            long
        )

    def check_condition(self, new_candle):
        ema = {
            'short': self.ema_short.value,
            'long': self.ema_long.value
        }

        self.strategy.add_message({
            'timestamp': new_candle[0],
            'open': new_candle[1],
            'high': new_candle[2],
            'low': new_candle[3],
            'close': new_candle[4],
            'volume': new_candle[5],
            'ema': ema,
            'positions': self.strategy.get_open_position_count(),
            'quote_balance': self.market.get_wallet_balance(),
            'base_balance': self.market.base_balance,
            'exit_balance': self.market.get_wallet_balance()
                + (self.market.base_balance * ((new_candle[2] + new_candle[3])/ 2))
        }, 'db')

        if ema['short'] > ema['long']:
            signal = 'buy'
        else:
            signal = 'sell'
            # NOTE: does seem to work better with a sell crossover
            # signal = 'hold'

        # NOTE: This does seem to work better than buying all the way up
        # Also it seems better to up the limit and only buy on the first signal
        if signal == self.last_signal and self.repeat_count < self.repeat_limit:
            self.repeat_count = self.repeat_count + 1
            self.last_signal = signal
            return signal

        if signal != self.last_signal:
            self.repeat_count = 0
            self.last_signal = signal
            return signal

        self.last_signal = signal
        return 'hold'
