from kryptobot.bot import Bot
from kryptobot.strategies.poc_strategy import PocStrategy

strategy = PocStrategy("5m", 'cryptopia', 'ETH', 'BTC', True, 12, 96, sim_balance=10)
# strategy = PocStrategy("5m", 'bittrex', 'ETH', 'BTC', True, 12, 96, sim_balance=10)
# strategy = PocStrategy("5m", 'binance', 'ETH', 'BTC', True, 12, 96, sim_balance=10)
bot = Bot(strategy)
bot.start()
