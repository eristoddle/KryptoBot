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
            '{start_date}'::timestamp,
            '{end_date}', '{series_interval}') AS date
        LEFT OUTER JOIN
          (SELECT
             ohlcv.timestamp as ts
           FROM ohlcv
           WHERE
             timestamp >= '{start_date}'
             and timestamp < '{end_date}'
             and exchange = '{exchange}'
             and pair = '{pair}'
             and interval = '{interval}') results
        ON (date = results.ts)
        where results.ts is null'''

    formatted_query = query.format(
        start_date=start_date,
        end_date=end_date,
        series_interval=series_interval,
        interval=interval,
        exchange=exchange,
        pair=pair
    )

    return session.execute(
        formatted_query
    ).fetchall()
