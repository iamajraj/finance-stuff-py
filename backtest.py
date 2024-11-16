# backtesting with 20 day and 50 day SMAs and golden/death cross

import matplotlib.pyplot as plt
import yfinance as yf

stock_data = yf.download("AAPL", start="2023-01-01", end="2023-12-31")

stock_data["SMA_20"] = stock_data['Close'].rolling(window=20).mean()
stock_data["SMA_50"] = stock_data['Close'].rolling(window=50).mean()

stock_data["Signal"] = 0
stock_data.loc[stock_data['SMA_20'] > stock_data['SMA_50'], 'Signal'] = 1
stock_data.loc[stock_data['SMA_20'] < stock_data['SMA_50'], 'Signal'] = -1

initial_capital = 10000
shares = 0
capital = initial_capital
portfolio_value = []
buy_dates = []
sell_dates = []

for i in range(1, len(stock_data)):
  if stock_data['Signal'].iloc[i] == 1 and stock_data['Signal'].iloc[i-1] != 1:
    shares = capital // stock_data['Close'].iloc[i]
    capital -= shares * stock_data['Close'].iloc[i]
    buy_dates.append(stock_data.index[i])
    print(f"Buy on {stock_data.index[i].date()} at {stock_data['Close'].iloc[i]}")
  
  elif stock_data['Signal'].iloc[i] == -1 and stock_data['Signal'].iloc[i-1] != -1:
    capital += shares * stock_data['Close'].iloc[i]
    shares = 0
    sell_dates.append(stock_data.index[i])
    print(f"Sell on {stock_data.index[i].date()} at {stock_data['Close'].iloc[i]}")

  portfolio_value.append(capital + shares * stock_data['Close'].iloc[i])

final_value = capital + shares * stock_data['Close'].iloc[-1]
print(f"\nInitial Capital: {initial_capital}")
print(f"Final Capital: {final_value}")
print(f"Net Profit: {final_value - initial_capital}")

plt.figure(figsize=(12,6))
plt.plot(stock_data['Close'], label="AAPL Closing Price", color="blue")
plt.scatter(buy_dates, stock_data.loc[buy_dates, 'Close'], label='Buy Signal', marker='^', color="green", s=100)
plt.scatter(sell_dates, stock_data.loc[sell_dates, 'Close'], label='Sell Signal', marker='v', color="red", s=100)
plt.title("AAPL Trading Strategy with Golden/Death Cross")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()