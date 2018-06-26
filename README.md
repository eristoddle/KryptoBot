# KryptoBot

A fork of Titan: https://github.com/Denton24646/Titan with a lot of changes.

I am writing a cryptocurrency portfolio and trading dashboard maybe for production or maybe just for me. I was working on the read-only wallets when I realized the market was looking better and I better focus on the trading part of the app. I realized that I didn't want to roll my own trading mechanism directly into my dashboard. So I went to look for a library. It was a toss up between the [Titan platform](https://github.com/Denton24646/Titan) and [Enigma Catalyst](https://github.com/enigmampc/catalyst).

What I liked about Titan was the granularity of everything and also almost complete ccxt integration. What I liked about enigma was backtesting although the back testing currently only on 3 crypto exchanges.

So I went with Titan, but had to fork it in order to make it installable by pip. I kept the wiki page for the original structure, which I still use for the market, strategy, signal and indicator objects. That's the granular part I liked. On the way to creating a library, I got to know how it worked and had to refactor a few things. Then I started adding features...

In the end, this will be a whole new project. It is in very active development by me right now, so the code base will change frequently.

## Added

- Uses SQL Alchemy models now
- DB connection and api keys configurable on app launch through json file or programmatically for multi tenant apps
- Added one way of monkey patching missing ccxt functionality(for Cryptopia candles specifically)
- Working optional Celery into the app so it can be as distributed as you want it to be

## Working On

- Harvester jobs that launch strategies
- Integration of enigma catalyst (Celery made this project so easy, this part is cake)
- Bot integration (i.e. telegram) for interactive strategy launch decisions
- Arbitrage strategies
- Price triangulation for optimal trades
- Portfolio management and portfolio context for strategies
- Backtesting
- Machine learning capabilities
- Sentiment analysis capabilities
- Maybe a half-assed dashboard, because I tired of watching workers scrolling to see what is happening and it can't be full-assed if that is what my other app is supposed to do

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
from kryptobot.bots.multi_bot import MultiBot
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

- Run `docker-compose up` to bring up the network with these images
    - jupyter
    - redis
    - timescale
    - all workers
- Go to http://0.0.0.0:8888/lab

## Install with pip

Right now the project is in flux, which is why it is not listed with pip.
I also have yet to figure out how to import workers once they are installed with pip.
So for now the best way to work with it is directly by cloning or forking and cloning
if you want to contribute.

`pip install git+https://github.com/eristoddle/KryptoBot.git`

or

Clone the project. Then run:

`pip install -e .`

in the main directory.

## More docs to come

I will be writing more docs once there is more functionality. For now, I have
embedded a lot of docs and notes in the Jupyter notebooks in the notebooks folder.
