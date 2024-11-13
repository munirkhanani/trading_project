import asyncio
import websockets
import json
import uuid

last_day_data = None

connected_clients = set()

async def process_data(ws):
    connected_clients.add(ws)
    try:
        async for message in ws:
            for client in connected_clients:
                print("Received from server:", message)
                # Process the message and create a response
                response = process_message(message)
                print("Sending to client:", message)  # Add this line for debugging
                await client.send(message)
            # handle_data(message)
    except Exception as e:
        print('the following exceptions occured: ', e)
    finally:
        # Unregister client on disconnect
        connected_clients.remove(ws)

def process_message(message):
    global last_day_data
    data = json.loads(message)
    open_price = data.get('Open')
    buy_price = 0

    if last_day_data is not None and open_price > last_day_data['High']:
        buy_price = open_price
        # print('the buy price is :' , buy_price)
        # Simulate some processing logic
        processed_data = {
            "order_id": str(uuid.uuid4()),
            "status": "processed",
            "buy_price": buy_price
        }
        last_day_data = data
        print('-----------------------------')
        print(last_day_data)
        print('-----------------------------')
        return json.dumps(processed_data)
    else:
        last_day_data = data
        print('-----------------------------')
        print(last_day_data)
        print('-----------------------------')
        return 'no buyng yet'
        
async def main():
    server = await websockets.serve(process_data, 'localhost', 8766)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
