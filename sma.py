import matplotlib.pyplot as plt
import yfinance as yf

stock_data = yf.download("AAPL", start="2023-01-01", end="2023-12-31")

stock_data["SMA_20"] = stock_data['Close'].rolling(window=20).mean()
stock_data["SMA_50"] = stock_data['Close'].rolling(window=50).mean()

plt.figure(figsize=(12, 6))
plt.plot(stock_data['Close'], label="AAPL Closing Price", color="blue")
plt.plot(stock_data['SMA_20'], label="20-Day SMA", color="orange")
plt.plot(stock_data['SMA_50'], label="50-Day SMA", color="green")
plt.title("AAPL Closing Price with 20 day and 50 day SMAs")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid()
plt.show()

stock_data["Signal"] = 0

stock_data.loc[stock_data['SMA_20'] > stock_data['SMA_50'], 'Signal'] = 1
stock_data.loc[stock_data['SMA_20'] < stock_data['SMA_50'], 'Signal'] = -1

golden_cross_dates = stock_data[(stock_data['Signal'] == 1) & (stock_data['Signal'].shift() != 1)].index
death_cross_dates = stock_data[(stock_data['Signal'] == -1) & (stock_data['Signal'].shift() != -1)].index

print("Golden Cross Dates:")
print(golden_cross_dates)
print("\nDeath Cross Dates:")
print(death_cross_dates)