import time as true_time
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime
from datetime import timedelta
from configparser import ConfigParser

from pyrobot.robot import PyRobot
from pyrobot.indicator import Indicators

# Grab the config file valuse
Config = ConfigParser()
Config.read('configs/config.ini')

CLIENT_ID = Config.get('main', 'CLIENT_ID')
REDIRECT_URI = Config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = Config.get('main', 'JSON_PATH')
ACCOUNT_NUMBER = Config.get('main', 'ACCOUNT_NUMBER')

# Initialize the robot.
trading_robot = PyRobot(
    client_id = CLIENT_ID,
    redirect_uri = REDIRECT_URI,
    credentials_path = CREDENTIALS_PATH,
    trading_account = ACCOUNT_NUMBER,
    paper_trading = True
)

# Create a new portfolio.
trading_robot_portfolio = trading_robot.create_portfolio()

# Add multi position to our portfolio.
multi_position = [
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'TSLA',
        'purchase_date': '2023-01-21'
    },
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'SQ',
        'purchase_data': '2023-01-21'
    }
]

# Add those positions to the portfolio.
new_positions = trading_robot.portfolio.add_positions(positions=multi_position)
pprint.pprint(new_positions)

# Add a single position to the portfolio.
trading_robot.portfolio.add_position(
    symbol='MSFT',
    quantity=10,
    purchase_price=10.00,
    asset_type='equity',
    purchase_date='2023-04-01'
    )
pprint.pprint(trading_robot.portfolio.positions)

# Check to see if the regular market is open.
if trading_robot.regular_market_open:
    print('Reguler Market Open')
else:
    print('Regular Market Not Open')

# Check to see if the regular Market is open.
if trading_robot.per_market_open:
    print('Pre Market Open')
else:
    print('Pre Market Not Open')

# Check to see if the post Market is open.
if trading_robot.per_market_open:
    print('Post Market Open')
else:
    print('Post Market Not Open')

# Grab the current quotes in our portfolio.
current_quotes = trading_robot.grab_current_quotes()
pprint.pprint(current_quotes)

# Define our date range.
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

# Grabe the historical prices.
historical_prices = trading_robot.grab_historical_prices(
    start=start_date,
    end=end_date,
    bar_size=1,
    bar_type='minute'
)

# Convert the data into a StockFrame
stock_frame = trading_robot.create_stock_frame(data=historical_prices['aggregated'])

# Print the head of the StokFrame.
pprint.pprint(stock_frame.stock.head(n=20))


# Create a new Trade Object.
new_trade = trading_robot.create_trade(
    trade_id='long_msft',
    enter_or_exit='enter',
    long_or_short='long',
    order_type='lmt',
    price=150.00
)

# Make it Good Till Cancel.
new_trade.good_till_cancel(cancel_time=datetime.now() + timedelta(minutes=90))

# Change the session
new_trade.modify_session(session='am')

# Add an Order Leg.
new_trade.instrument(
    symbol='MSFT',
    quantity=2,
    asset_type='EQUITY'
)

# Add a Stop Loss Order with the Main Order.
new_trade.add_stop_loss(
    stop_size=.10,
    percentage=False
)

# print out the order.
pprint.pprint(new_trade.order)


# Create a new indicator client
Indicator_client = Indicators(price_data_farme=stock_frame)

# Add the RSI indicator
Indicator_client.rsi(period=14)

# Add a 200-day simple moving average.
Indicator_client.sma(period=200)

# Add a 50-day exponential moving average.
Indicator_client.ema(period=50)

# Add a signal to check for.
Indicator_client.set_indicator_signal(
    indicator='rsi',
    buy=40.0,
    sell=20.0,
    condition_buy=operator.ge,
    condition_sell=operator.le
)

# Define a trade dictionary
trades_dict = {
    'MSFT':{
        'trade_func': trading_robot.trades['long_msft'],
        'trade_id': trading_robot.trades['long_msft'].trade_id
    }
}

while True:

    # Grab the latest bar.
    latest_bars = trading_robot.get_latest_bars()

    # Add those bars to the StockFrame
    stock_frame.add_rows(data=latest_bars)

    # Refresh the indicators
    Indicator_client.refresh()

    print("="*50)
    print("Current StockFrame")
    print("-"*50)
    print(stock_frame.symbol_groups.tail())
    print("-"*50)
    print("")

    # Check for signals.
    signals = Indicator_client.check_signals()
    
    # Execute Trades.
    trading_robot.execute_signals(signals=signals, trades_to_execute=trades_dict)

    # Grab the last bar, keep in mind this is after adding the new rows.
    last_bar_timestamp = trading_robot.stock_frame.farme.tail(1).index_get_level_values(1)

    # wait till the next bar.
    trading_robot.wait_till_next_bar(last_bar_timestamp=last_bar_timestamp)