import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import yfinance as yf
from flask import Flask, request
import io

matplotlib.use("agg")

app = Flask(__name__)
app.static_folder = "views"

@app.get("/")
def index():
  return app.send_static_file("index.html")

@app.post("/plot")
def plotChart():
  ticker = request.form.get("ticker")
  start = request.form.get("start")
  end = request.form.get("end")

  stock_data = yf.download(ticker, start=start, end=end)  
  stock_data["Close"].plot(title=f"{ticker} Stock Price", figsize=(10,5))

  buf = io.BytesIO()
  plt.savefig(buf, format="png")
  buf.seek(0)
  plt.close()
  return app.response_class(buf.getvalue(), mimetype="image/png")

print("Running server on port 8000")
app.run(debug=True, port=8000)