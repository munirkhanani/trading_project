import pandas as pd
import data_storage
import websockets
import asyncio
import json
from indicators import calculate_rsi , calculate_sma
# Load the CSV data into a DataFrame
df = pd.read_csv('ohlcv.csv')
df['Date'] = pd.to_datetime(df['date'])

async def simulate_data_stream(interval=0.1):
      # Calculate indicators for the entire dataset
    df['RSI'] = calculate_rsi(df['close'])
    df['SMA_40'] = calculate_sma(df['close'], 40)
    df['SMA_50'] = calculate_sma(df['close'], 50)
    df['SMA_200'] = calculate_sma(df['close'], 200)

    url = 'ws://localhost:8765'
    async with websockets.connect(url) as ws:
        for _, row in df.iterrows():
            # Lock the data_storage before updating
            with data_storage.data_lock:
                data_storage.current_data = {
                    "Date": row['date'],
                    "Open": row['open'],
                    "High": row['high'],
                    "Low": row['low'],
                    "Close": row['close'],
                    "Volume": row['volume'],
                    "RSI": row['RSI'] if not pd.isna(row['RSI']) else None,
                    "SMA_40": row['SMA_40'] if not pd.isna(row['SMA_40']) else None,
                    "SMA_50": row['SMA_50'] if not pd.isna(row['SMA_50']) else None,
                    "SMA_200": row['SMA_200'] if not pd.isna(row['SMA_200']) else None
                }
            
            data = json.dumps(data_storage.current_data)
            await ws.send(data)
            await asyncio.sleep(interval)  # Use asyncio.sleep to avoid blocking the event loop

async def send_df():
    await simulate_data_stream()

if __name__ == '__main__':
    asyncio.run(send_df())
