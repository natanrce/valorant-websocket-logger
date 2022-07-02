import os
import ssl
import base64
import asyncio
import websockets

async def connect_websocket(port, password):
    url = f'wss://127.0.0.1:{port}'
    password_secret = encode_password(password)
    
    headers = {
        'Authorization': 'Basic ' + password_secret, 
    }
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(url, ssl=ssl_context, extra_headers=headers) as ws:
        await ws.send("[5, \"OnJsonApiEvent\"]")

        while True:
            response = await ws.recv()
            
            if len(response) > 0:
                print(response)

def main():
    lockfile = {}
    
    lockfile_path = os.path.join(
        os.getenv('LOCALAPPDATA'),
        r'Riot Games\Riot Client\Config\lockfile'
    )
    
    try:
        with open(lockfile_path, 'r') as file:
            lines = file.read()
            data = lines.split(':')
            
            keys = ['name', 'PID', 'port', 'password', 'protocol']
            lockfile = dict(zip(keys, data))
    except:
        print('No lockfile found')
    
    port = lockfile['port']
    password = lockfile['password']
    
    asyncio.get_event_loop().run_until_complete(connect_websocket(port, password))
    asyncio.get_event_loop().run_forever()

def encode_password(password):
    return base64.b64encode(('riot:' + password).encode()).decode()

if __name__ == '__main__':
    main()
