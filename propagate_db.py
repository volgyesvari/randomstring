import asyncio
import aiohttp
import random
import time
import json
from typing import Any


URL = "http://localhost:8000/measurement"
METRIC_TYPES = ["temperature", "humidity", "windSpeed", "pressure"]
SENSOR_ID_MIN = 1
SENSOR_ID_MAX = 10
NUM_RECORDS = 500
CONCURRENCY_LIMIT = 10

START_TIMESTAMP = int(time.time())

SEMAPHORE = asyncio.Semaphore(CONCURRENCY_LIMIT)

def generate_measurement_data(sensor_id, metric_type, current_timestamp):
    metric_value = 0

    if metric_type == "temperature":
        metric_value = round(random.uniform(-10.0, 40.0), 2)
    elif metric_type == "humidity":
        metric_value = round(random.uniform(0.0, 100.0), 2)
    elif metric_type == "windSpeed":
        metric_value = round(random.uniform(0.0, 50.0), 2)
    elif metric_type == "pressure":
        metric_value = round(random.uniform(950.0, 1050.0), 2)

    data = {
        "sensorId": sensor_id,
        "metricType": metric_type,
        "metricValue": metric_value,
        "timestamp": current_timestamp
    }
    return data

async def send_single_request(session: aiohttp.ClientSession, data: dict[str, Any], record_num: int):
    async with SEMAPHORE:
        headers = {'Content-Type': 'application/json'}
        try:
            async with session.post(URL, data=json.dumps(data), headers=headers, timeout=10) as response:
                if response.status in [200, 201, 202]:
                    return True
                else:
                    print(f"#{record_num} failed with status {response.status}: {await response.text()}")
                    return False

        except asyncio.TimeoutError:
            print(f"#{record_num} failed due to timeout.")
            return False
        except aiohttp.ClientError as e:
            print(f"#{record_num} failed due to client error: {e}")
            return False

async def load_data_to_db():
    print(f"Starting to send {NUM_RECORDS} records to {URL}...")

    all_data_to_insert: list[dict[str, Any]] = []
    current_timestamp = START_TIMESTAMP

    for i in range(1, NUM_RECORDS + 1):
        sensor_id = random.randint(SENSOR_ID_MIN, SENSOR_ID_MAX)
        metric_type = random.choice(METRIC_TYPES)

        data = generate_measurement_data(sensor_id, metric_type, current_timestamp)
        all_data_to_insert.append(data)

        current_timestamp += 5

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, data in enumerate(all_data_to_insert):
            task = asyncio.create_task(send_single_request(session, data, i + 1))
            tasks.append(task)

        results = await asyncio.gather(*tasks)


    success_count = sum(results)
    failure_count = NUM_RECORDS - success_count
    print(f"Total: {NUM_RECORDS}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")

if __name__ == "__main__":
    asyncio.run(load_data_to_db())