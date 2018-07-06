import re


def ccxt_to_series_interval(interval):
    match = re.match(r"([0-9]+)([a-z]+)", interval, re.I)
    if match:
        items = match.groups()
        if items[1] == 'm':
            return items[0] + ' minutes'
        if items[1] == 'h':
            return items[0] + ' hours'


def get_candle_gaps(session, start_date, end_date, interval, exchange, pair):
    series_interval = ccxt_to_series_interval(interval)
    query = '''SELECT
          date
        FROM
         generate_series(
            ':start'::timestamp,
            ':end', ':series_interval') AS date
        LEFT OUTER JOIN
          (SELECT
             ohlcv.timestamp as ts
           FROM ohlcv
           WHERE
             timestamp >= ':start'
             and timestamp < ':end'
             and exchange = ':exchange'
             and pair = ':pair'
             and interval = ':interval') results
        ON (date = results.ts)
        where results.ts is null'''

    result = session.execute(
        query,
        {
            "start": start_date,
            "end": end_date,
            "series_interval": series_interval,
            "interval": interval,
            "exchange": exchange,
            "pair": pair,
        }
    )
    return result
