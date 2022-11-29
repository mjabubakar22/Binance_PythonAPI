# Crypto Trading bot using Binance API and Python:
This is a short explanation regarding the project,
Using the Binance API, I created a trading algorithm that enters a long and short position by defining
a function that takes 5 arguments, coin (crypto pair to be traded), take_profit (At what point to take
profit in %), Losing_trade_lossII(At what point to take a loss in %), trail(At what point to start the
trailing stop)


In the first few lines of code inside the function, I cancel any open order which is just a good practice
I like doing before running a trading algorithm, then it checks if I have any open position (which
there should be none), then it will send a long and short market order to the exchange and
immediately they will be executed at the market price. At this point, I will now be in a long/short
position.


Then, the bot will calculate at what price I should sell to take profit, to cut my losses, and where my
trailing stop should be activated, once calculated the respective order will be sent for both positions,
hence each position will have a take profit price, stop loss price and trailing stop price
Using the while function the algorithm will run in an infinite loop and creates a log that I can monitor
to not only check the current status of my trading account but also to see whether there are no
issues with my bot (I think of it as a heartbeat for my bot).


if I’m in a long and short position it will print out ‘In long/Short position’. if I’m in a winning trade it
will print out which direction it is whether it’s a long or short winning position. Once my winning
position either hits the take profit or trailing stop the bot runs again repeating the process!
