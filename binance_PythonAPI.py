import pandas as pd
from binance.client import Client
from binance.enums import *
from binance import ThreadedWebsocketManager
import time
pd.options.display.max_columns = None

key = 
secret = 
client = Client(api_key=key,api_secret=secret)

def long_short(coin,Quantity,take_profit,losing_trade_loss,trail):
    position2 = pd.DataFrame(client.futures_position_information(symbol=coin,recvWindow=59999))
    not_long_and_short = (position2['entryPrice'][1]== '0.0' and position2['entryPrice'][2] == '0.0') # if not in position long AND short, then
    in_long = (position2['entryPrice'][1] !='0.0' and position2['entryPrice'][2]== '0.0')
    in_short = (position2['entryPrice'][2] !='0.0' and position2['entryPrice'][1]== '0.0')
 
    if not_long_and_short: #not_in_long and not_in_short: 
        print(client.futures_cancel_all_open_orders(symbol=coin,recvWindow=59999))
          #ENTER LONG AND SHORT POSITIONS 
        open_long = client.futures_create_order(
            symbol=coin,
            side='BUY',
            positionSide='LONG', 
            type='MARKET',
            quantity=Quantity,
            recvWindow=59999)

        open_short = client.futures_create_order(
            symbol=coin,
            side='SELL',
            positionSide='SHORT', 
            type='MARKET',
            quantity=Quantity,
            recvWindow=59999)

            #CHECK OPEN POSITIONS
        position = pd.DataFrame(client.futures_position_information(symbol=coin,recvWindow=59999))
        long_price = position['entryPrice'][1]
        long_notional_value = position['notional'][1]
        short_price = position['entryPrice'][2]
        short_notional_value = position['notional'][2]

            #ADD STOP LOSS,TAKE PROFIT AND TRAILING STOP
            #CALCULATE STOP PRICEs:
            #LONG STOP:
        long_entry_price = float(position['entryPrice'][1]) #transform price from string to float #1 is long, 2 is short
        long_lev = float(position['leverage'][1])
        long_max_position_loss = losing_trade_loss #the percentage you wanna lose in your position before stopping losing trade
        long_max_pos_loss_non_lev = long_max_position_loss/long_lev #non lev loss %
        long_stop_loss = str(round(long_entry_price - (long_entry_price * long_max_pos_loss_non_lev),2)) 

            #SHORT STOP:
        short_entry_price = float(position['entryPrice'][2]) #transform price from string to float #1 is long, 2 is short
        short_lev = float(position['leverage'][2])
        short_max_position_loss = losing_trade_loss #the percentage you wanna lose in your position before stopping losing trade
        short_max_pos_loss_non_lev = short_max_position_loss/short_lev #non lev loss %
        short_stop_loss = str(round(short_entry_price + (short_entry_price * short_max_pos_loss_non_lev),2))
             
            #LONG TAKE PROFIT:
        long_take_profit_non_lev = take_profit/long_lev
        long_take_profit =   str(round(long_entry_price + (long_entry_price * long_take_profit_non_lev),2))

            #LONG TAKE PROFIT:
        short_take_profit_non_lev = take_profit/short_lev
        short_take_profit =   str(round(short_entry_price - (short_entry_price * short_take_profit_non_lev),2))

            #PLACE STOP LOSSES
            #LONG
        long_stop = client.futures_create_order(
            symbol=coin,
            side='SELL',
            positionSide='LONG', 
            type='STOP_MARKET',
            quantity=Quantity,
            stopPrice=long_stop_loss,
            closePosition=True,
            #reduceOnly='true',
            recvWindow=59999)    

           #SHORT
        short_stop = client.futures_create_order(
            symbol=coin,
            side='BUY',
            positionSide='SHORT', 
            type='STOP_MARKET',
            quantity=Quantity,
            stopPrice=short_stop_loss,
            #reduceOnly='true',
            closePosition=True,
            recvWindow=59999)

            #PLACE TAKE PROFITS
            #LONG
        long_profit = client.futures_create_order(
            symbol=coin,
            side='SELL',
            positionSide='LONG', 
            type='TAKE_PROFIT_MARKET',
            quantity=Quantity,
            stopPrice=long_take_profit,
            closePosition=True,
            #reduceOnly='true',
            recvWindow=59999)    

           #SHORT
        short_profit = client.futures_create_order(
            symbol=coin,
            side='BUY',
            positionSide='SHORT', 
            type='TAKE_PROFIT_MARKET',
            quantity=Quantity,
            stopPrice=short_take_profit,
            #reduceOnly='true',
            closePosition=True,
            recvWindow=59999)


            #PLACE TRAILING STOP
            #LONG
        TSL_long = client.futures_create_order(
            symbol=coin,
            side='SELL',
            positionSide='LONG',
            type="TRAILING_STOP_MARKET",
            callbackRate=trail,         
            quantity=Quantity,
            activationPrice=short_stop_loss,
            recvWindow=59999)

         #SHORT
        TSL_short = client.futures_create_order(
            symbol=coin,
            side='BUY',
            positionSide='SHORT',
            type="TRAILING_STOP_MARKET",
            callbackRate=trail,         
            quantity=Quantity,
            activationPrice=long_stop_loss,
            recvWindow=59999)

            #PRINT ALL RELEVANT INFO
        open_orders = pd.DataFrame(client.futures_get_open_orders(recvWindow=59999))

        print('LONG DETAILS:')
        print(f'Long Entry price :{long_price}')
        print(f'Long Notional Value :{long_notional_value}')

        print('\nSHORT DETAILS:')
        print(f'Short Entry price :{short_price}')
        print(f'Short Notional Value :{short_notional_value}')
        print(open_orders[['positionSide','type','activatePrice','stopPrice']])    
         
    elif(in_short):
        print('In winning trade: SHORT')
    elif(in_long):
        print('In winning trade: LONG')
    else:
        print('In long/short position') 

#run code infinit
while True:
    long_short('ETHUSDT',0.005,0.10,0.95,1.5)
    time.sleep(5)
