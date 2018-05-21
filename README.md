# kryptobot

A fork of Titan: https://github.com/Denton24646/Titan with changes to make it importable as a library among other things

## One way to run

```python
from kryptobot import database
from kryptobot.strategies.poc_strategy import PocStrategy

def start_strategy():
    strategy = PocStrategy("5m", 'cryptopia', 'ETH', 'BTC', True, 100, 700,  sim_balance=10)
    strategy.run_simulation()
    strategy.start()

def start():
    try:
        database.create_tables()
        start_strategy()

    except Exception as e:
        print(e)
    
    finally:
        database.engine.dispose()


start()
```

## Another way

```python
from kryptobot.bot import Bot

from kryptobot.strategies.poc_strategy import PocStrategy

from os import getcwd

config = getcwd() + '/config.json'

strategy = PocStrategy("5m", 'cryptopia', 'ETH', 'BTC', True, 12, 96, sim_balance=10)

bot = Bot(strategy, config=config)

bot.start()

```



## More docs to come

I will be writing more docs once there is more functionality
