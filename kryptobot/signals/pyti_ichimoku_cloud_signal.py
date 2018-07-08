from ..signals.base_signal_generator import BaseSignalGenerator
from ..ta.pyti_ichimoku_cloud import PytiIchimokuCloud


# TODO: More research
# http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud
class PytiIchimokuCloudSignal(BaseSignalGenerator):

    def __init__(self, market, interval, params, strategy):
        super().__init__(market, interval, strategy)
        pyti_params = {
            'market': market,
            'interval': interval
        }
        self.tenkansen = PytiIchimokuCloud(
            market,
            interval,
            pyti_params.update({
                'periods': 9,
                'params': {'indicator': 'tenkansen'}
            })
        )
        self.kijunsen = PytiIchimokuCloud(
            market,
            interval,
            pyti_params.update({
                'periods': 26,
                'params': {'indicator': 'kijunsen'}
            })
        )
        self.senkou_span_a = PytiIchimokuCloud(
            market,
            interval,
            pyti_params.update({
                'periods': 52,
                'params': {'indicator': 'senkou_span_a'}
            })
        )
        self.senkou_span_b = PytiIchimokuCloud(
            market,
            interval,
            pyti_params.update({
                'periods': 52,
                'params': {'indicator': 'senkou_span_b'}
            })
        )
        self.chikou_span = PytiIchimokuCloud(
            market,
            interval,
            pyti_params.update({
                'periods': 52,
                'params': {'indicator': 'chikou_span'}
            })
        )

    # TODO: Not sure how to generate a signal with this one or even if I have the periods right
    # Also have to update the indicators next_calculation method to account for the indicator param
    def check_condition(self, new_candle):
        self.strategy.add_message("Getting PytiIchimokuCloud Signal")
        print('tenkansen', self.tenkansen.value)
        print('kijunsen', self.kijunsen.value)
        print('senkou_span_a', self.atr.senkou_span_a)
        print('senkou_span_b', self.atrp.senkou_span_b)
        print('chikou_span', self.chikou_span.value)

        self.strategy.add_message({
            'ichimoku_cloud': {
                'tenkansen': self.tenkansen.value,
                'kijunsen': self.kijunsen.value,
                'senkou_span_a': self.atr.senkou_span_a,
                'senkou_span_b': self.atrp.senkou_span_b,
                'chikou_span': self.chikou_span.value
            }
        }, 'db')

        return False
