import asyncio
import argparse
import json
import time
from pathlib import Path

import httpx



async def check_url(client, url, timeout):
    start_time = time.perf_counter()
    try:
        response = await client.get(url, timeout=timeout)
    except httpx.TimeoutException:
        return f"{url}: TIMEOUT"
    except httpx.ConnectError:
        return f"{url}: CONNECTION_ERROR"

    end_time = time.perf_counter()
    response_time_ms = (end_time - start_time) * 1000
    return f"{url}: {response.status_code}, {response_time_ms:.2f} ms"


async def main(input_file, timeout):
    with input_file.open(encoding="utf-8") as file:
        urls = json.load(file)

    async with httpx.AsyncClient() as client:
        coroutines = [check_url(client, url, timeout) for url in urls]
        start_total_time = time.perf_counter()
        results = await asyncio.gather(*coroutines)
        end_total_time = time.perf_counter()
        total_time_ms = (end_total_time - start_total_time) * 1000

        for result in results:
            print(result)

        print(f"Total time: {total_time_ms:.2f} ms")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    if not args.input_file.exists():
        parser.error(f"input file does not exist: {args.input_file}")
    if not args.input_file.is_file():
        parser.error(f"input path is not a file: {args.input_file}")

    return args


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.input_file, args.timeout))
