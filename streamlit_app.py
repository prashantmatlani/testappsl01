import streamlit as st

st.title("🎈 New Streamlit app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)



# Canadian stock tickers (on TSX)
#.TO is for TSX (Toronto Stock Exchange)
#.V is for TSX Venture Exchange (e.g., FIRE.V)

#Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 4h, 1d, 5d, 1wk, 1mo, 3mo]
#uncomment print(tabulate(data, header="keys"..... to print tabulated data


import sys
import yfinance as yf
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import warnings
warnings.filterwarnings("ignore")

#symbols = ["RY.TO", "SHOP.TO", "TD.TO", "ENB.TO"]  # RBC, Shopify, TD Bank, Enbridge

#symbols = ["PTNM"]
#symbols = ["AXISBANK.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "MOTHERSON.NS", "RPOWER.NS", "FILATFASH.NS", "JITFINFRA.NS", "ASAHISONG.NS", "PARADEEP.NS", "BLUECOAST.NS"]
#symbols = ["SALSTEEL.NS", "SURANI.NS"]
#symbols = ["SETUINFRA.NS"]
#symbols = ["ALPHAGEO.NS"]
#symbols = ["TFCILTD.NS"]
#symbols = ["ADANIENT.NS", "HDFCBANK.NS"]
#symbols = ["ADANIENT.NS"]
#symbols = ["GODREJPROP.NS"]
#symbols = ["YESBANK.NS", "UJJIVANSFB.NS", "ITC.NS", "ITCHOTELS.NS", "TCS.NS", "DEEPAKNTR.NS", "RELIANCE.NS", "SNOWMAN.NS"]
symbols = ["AONEGOLD.NS", "VIJAYPD-SM.NS"]

#symbols = ["NIFTYBANK.NS"]

#symbols = ["NIFTY100LOWVOLATILITY30.NS", "NIFTYALPHALOW-VOLATILITY30.NS", "NIFTYALPHAQUALITYLOW-VOLATILITY30.NS", "NIFTYALPHAQUALITYVALUELOW-VOLATILITY30.NS", "NIFTYLOWVOLATILITY50.NS", "NIFTYQUALITYLOW-VOLATILITY30.NS", "NIFTY500LOWVOLATILITY50.NS"]




period = "44d"
interval = "1d"

usin = True
#usin = False
#symex = True
symex = False


#"""# -------------------- LOAD SYMBOLS FROM EXCEL --------------------

if symex:

    excel_path = r"C:\Users\wd052\OneDrive\Desktop\00\Works\PB\Excel\sym01.xlsx"

    # Read Excel starting from A2 (skip first row if it’s a header)
    symbols_df = pd.read_excel(excel_path, header=None, usecols=[0], skiprows=1, names=["Symbol"])

    # Drop any empty cells
    symbols_df = symbols_df.dropna(subset=["Symbol"])

    # Display how many symbols are available
    total_symbols = len(symbols_df)
    print(f"\n📘 Found {total_symbols} symbols in {excel_path} (starting A2).")
    print(symbols_df.head(10))  # preview first 10

    # Ask user how many symbols to use
    try:
        n = int(input(f"\nEnter number of symbols to use (max {total_symbols}): "))
        if n > total_symbols or n <= 0:
            print(f"⚠️ Invalid number, using all {total_symbols} symbols instead.")
            n = total_symbols
    except ValueError:
        print(f"⚠️ Invalid input, using all {total_symbols} symbols.")
        n = total_symbols

    # Slice top N and clean up symbol list
    symbols = symbols_df["Symbol"].head(n).astype(str).str.strip().tolist()
    # Append ".NS" if not already
    symbols = [s if s.endswith(".NS") else s + ".NS" for s in symbols]

    period = input("Enter Period: ") # user prompt - period input
    interval = input("Enter Interval: ") # user prompt - interval input

    if not period:
        period = "1d"
    if not interval:
        interval = "1d"

    print(f"\n✅ Using {len(symbols)} symbols: {symbols}")

#"""# -------------------- LOAD SYMBOLS FROM EXCEL - End Block --------------------



#"""# --------------- User Input ---------------

if usin:

    # Predefined Nifty50 heavyweights
    nifty50_heavyweights = [
        "RELIANCE.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "TCS.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "KOTAKBANK.NS"
    ]

    # -- Prompt user for single or multiple stock symbols (comma-separated)
    symbol_input = input("Enter Stock Symbol(s), separated by commas: ")
    #symbol_input = input("Enter stock symbols (comma separated, without .NS): ").strip()

    # -- Exchange Code
    exc = input("Enter Exchange Code, 'N' for NSE, 'B' for 'BSE': ")
    exc= exc.upper()

    period = input("Enter Period: ")
    #period = period + "d"
    interval = input("Enter Interval: ")
    #interval = interval + "d"

    #print(f"Entered Stock: {symbols}")
    #print(len(symbols)) # no. of Stocks to be queried from  the list
    #sys.exit()

    if symbol_input: #if user inputs
        # Convert input into a list, strip spaces, and append ".NS"/".BO" to each symbol
        if exc == "N":
            symbols = [sym.strip().upper() + ".NS" for sym in symbol_input.split(",")]
        else:
            symbols = [sym.strip().upper() + ".BO" for sym in symbol_input.split(",")]
    else:
        symbols = nifty50_heavyweights  # fallback if no input

    print(f"Entered Stock: {symbols}")

    if not period:
        period = "1d"
        #period = "7d"
    if not interval:
        interval = "1d"

#"""# --------------- User Input - End Block ---------------

all_results = []  # store results for all symbols
all_pivot_results = []  # store results for all symbols

# Fetch data for each
for symbol in symbols:
    data = yf.download(symbol, period=period, interval=interval)
    #print(f"data = yf.download({symbol}, period={period}, interval={interval})")
    #sys.exit()
    #data.reset_index(inplace=True)  # To include the date as a column

    # --- Handle MultiIndex Columns (common in yfinance) ---
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0].lower() for col in data.columns]
    else:
        data.columns = [col.lower() for col in data.columns]

    #print("✅ Normalized columns:", data.columns)

    # --- Prepare final DataFrame ---
    data["datetime"] = data.index
    data["symbol"] = symbol.replace(".NS", "")
    data = data[["datetime", "symbol", "open", "high", "low", "close", "volume"]]
    data = data.dropna()
    #data.reset_index(drop=True, inplace=True)

    # create a dataframe for price percentage change
    data_pc = pd.DataFrame({"pc": [(((data["close"] / data["close"].shift(1)) - 1) * 100)]})
    # get rid of NaN values from the dataframe
    data_pc = data_pc.dropna()

    #print(f" data pc info: {data_pc.info()}")
    #print(data["symbol"])
    #print(data["close"])
    #print(data["close"].shift(1))
    #print(((data["close"] / data["close"].shift(1)) - 1) * 100)
    #print(f"data pc drop na: \n{(((data["close"] / data["close"].shift(1)) - 1) * 100).dropna()}")
    #sys.exit()

    # dataframe excluded of percentage change
    data_c = data[["symbol", "close", "volume", "open", "high", "low"]]
    #print(data_c)
    #sys.exit()
    # concatenate the regular and percent change data frames
    #data_c = pd.concat([data_c[["symbol", "close"]], data_pc[["pc"]], data_c[["volume", "open", "high", "low"]]], axis=1)
    #data_c = pd.concat([data_c[["symbol", "close"]], data_pc[["pc"]]],axis=1)
    #horizontal_concat = pd.concat([df1, df2], axis=1)
    # get rid of NaN values from the concatenated dataframe
    #data_c=data_c.dropna()
    #print(data_c.sort_index(axis=0, ascending=False, inplace=True))
    #print(data_c.sort_values(by='Date', ascending=False))
    #sys.exit()


#"""
    all_results.append(data_c)
    #all_results.append(data_c_pd)

final_df = pd.concat(all_results, ignore_index=False)

# round values to two decimals
cols_to_round = final_df.select_dtypes(include=["float", "int"]).columns
final_df[cols_to_round] = final_df[cols_to_round].round(2)

#print(f" final df: {final_df}")

# reset index to include date, but sort (further) on actual index number descending (each corresponding to unique key (dte+symbol)) for propper sort (date+symbl)
final_df.reset_index(inplace=True)
#print(f"final df columns: {final_df.columns}")
#print(final_df.shape)
#sys.exit()
final_df.sort_index(axis=0, ascending=False, inplace=True)
#set date format post sorting by index descending
final_df['Date'] = final_df['Date'].dt.strftime('%Y-%m-%d')
print(f"\n")
print(tabulate(final_df, headers="keys", showindex=False))
#print(tabulate(final_df['symbol', 'close', 'volume', 'open', 'high', 'low'], headers="keys"))

#print(f"\nPrice today: \n{final_df}")
#final_df.groupby(['Date','symbol'], group_keys=False)
#final_df.sort_values(by='Date', ascending=False)
#final_df.sort_index(axis=0, ascending=False, inplace=True)
#print(f"\nPrice: \n{final_df.sort_values(by='Date', ascending=False)}")
#print(f"\nPrice: \n{final_df.sort_values(by=['Date','symbol'], ascending=[False, False])}")
#print(tabulate(final_df, headers="keys", showindex=True))



#print(tabulate(final_df, headers="keys", tablefmt="grid", showindex=True))
#"""
#print(f"\nPivot: \n{pivot_final_df}")

#print(f"\nLast run: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}\n")