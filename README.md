# KryptoBot

A fork of Titan: https://github.com/Denton24646/Titan with a lot of changes.

I am writing a crytptocurrency portfolio and trading dashboard maybe for production or maybe just for me. I was working on the read-only wallets when I realised the market was looking better and I better focus on the trading part of the app. I realized that I didn't want to roll my own trading mechanism directly into my dashboard. So I went to look for a library. It was a toss up between the [Titan platform](https://github.com/Denton24646/Titan) and [Enigma Catalyst](https://github.com/enigmampc/catalyst).

What I liked about Titan was the granularity of everything and also almost complete ccxt integration. What I liked about enigma was backtesting although the back testing currently only on 3 crypto exchanges.

So I went with Titan, but had to fork it in order to make it installable by pip. I kept the wiki page for the original structure, which I still use for the market, strategy, signal and indicator objects. That's the granular part I liked. On the way to creating a library, I got to know how it worked and had to refactor a few things. Then I started adding features...

In the end, this will be a whole new project. It is in very active development by me right now, so the code base will change frequently.

## Added

- Uses SQL Alchemy models now
- DB connection and api keys configurable on app launch through json file or programmatically by application for multiple users
- Added one way of monkey patching missing ccxt functionality(for Cryptopia candles specifically)
- Working optional Celery into the app so it can be as distributed as you want it to be

## Working On

- Harvester jobs that launch strategies
- Bot integration (i.e. telegram) for interactive strategy launch decisions
- Arbitrage strategies
- Price triangulation for optimal trades
- Portfolio management and portfolio context for strategies
- Backtesting
- Machine learning capabilities
- Sentiment analysis capabilities

## Running from bot classes

```python
from kryptobot.bots.bot import Bot
from kryptobot.strategies.poc_strategy import PocStrategy
from os import getcwd

# see config.example.json for structure
config = getcwd() + '/config.json'
strategy = PocStrategy("5m", 'cryptopia', 'ETH', 'BTC', True, 12, 96, sim_balance=10)
bot = Bot(strategy, config=config)
bot.start()

```



```python
from kryptobot.bots.multi_bot import Bot
from kryptobot.strategies.poc_strategy import PocStrategy

strategies = [
    PocStrategy("5m", 'cryptopia', 'ETH', 'BTC', True, 12, 96, sim_balance=10),
    PocStrategy("5m", 'bittrex', 'ETH', 'BTC', True, 12, 96, sim_balance=10)
]

# NOTE: without config, it uses a sqlite db
bot = MultiBot(strategies)
bot.start()

```

## Run with Docker and Jupyter Lab

Install Docker.

Run `docker-compose up`

Browse to http://0.0.0.0:8888/lab and use the token given in the docker console.

See the notebooks folder for mor examples of code. I have been committing my lab work to make up for the sparsity of docs.

## More docs to come

I will be writing more docs once there is more functionality
