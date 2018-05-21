# KryptoBot

A fork of Titan: https://github.com/Denton24646/Titan with changes to make it importable as a library among other things

## One way to run

```python
from kryptobot.bot import Bot

from kryptobot.strategies.poc_strategy import PocStrategy

from os import getcwd

config = getcwd() + '/config.json'

strategy = PocStrategy("5m", 'cryptopia', 'ETH', 'BTC', True, 12, 96, sim_balance=10)

bot = Bot(strategy, config=config)

bot.start()

```

## Run with Docker and Jupyter Lab


## More docs to come

I will be writing more docs once there is more functionality
