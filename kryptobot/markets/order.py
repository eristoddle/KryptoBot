import datetime
import time
import logging
from ..db.models import TradingOrder

logger = logging.getLogger(__name__)


class Order:
    """Class that represents an order. Order executes on instantiation by a thread pool"""
    def __init__(self, market, side, type, amount, price, session=None):
        self.market = market
        if session is not None:
            self.session = session()
        self.side = side
        self.type = type
        self.amount = amount
        self.price = price
        self.__order_receipt = None
        logger.info("Opening " + side + " order of " + amount + " " + self.market.base_currency)
        self.execute()

    def execute(self):
        if self.type == "limit":
            if self.side == "buy":
                self.__order_receipt = self.market.exchange.create_limit_buy_order(self.market.analysis_pair, self.amount, self.price)
                order = TradingOrder(
                    exchange=self.market.exchange.id,
                    pair=self.market.analysis_pair,
                    position='long',
                    amount=self.amount,
                    price=self.price,
                    simulated="live"
                )
                self.session.add(order)
                self.session.commit()
                self.session.close()
            elif self.side == "sell":
                self.__order_receipt = self.market.exchange.create_limit_sell_order(self.market.analysis_pair, self.amount, self.price)
                order = TradingOrder(
                    exchange=self.market.exchange.id,
                    pair=self.market.analysis_pair,
                    position='short',
                    amount=self.amount,
                    price=self.price,
                    simulated="live"
                )
                self.session.add(order)
                self.session.commit()
                self.session.close()
            else:
                logger.error("Invalid order side: " + self.side + ", specify 'buy' or 'sell' ")
        elif self.type == "market":
            logger.error("Market orders not available")
        else:
            logger.error("Invalid order type: " + self.type + ", specify 'limit' or 'market' ")

    def get_id(self):
        return self.__order_receipt.get().id

    def cancel(self):
        try:
            self.market.exchange.cancel_order(self.get_id())
        except:
            logger.error("Order cannot be canceled. Has already been filled")

    def is_open(self):
        return self.market.exchange.fetch_order(self.get_id())['remaining'] > 0

    def get_status(self):
        return self.market.exchange.fetch_order(self.get_id())['status']

    def get_amount_filled(self):
        return self.market.exchange.fetch_order(self.get_id())['filled']

    def get_amount_remaining(self):
        return self.market.exchange.fetch_order(self.get_id())['remaining']
