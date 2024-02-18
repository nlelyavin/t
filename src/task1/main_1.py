import asyncio
from typing import List

from aiohttp import ClientSession, ClientTimeout


async def request(method, url, **kwargs):
    async with ClientSession(timeout=ClientTimeout(60)) as client:
        async with client.request(method, url, **kwargs) as response:
            return await response.text()


async def parse(url: str, file_index: int) -> None:
    print(f'parse {url}')

    text = await request(method="GET", url=url,)

    try:
        with open(f'result/{file_index}_file.html', mode='a', encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(e)


async def main():

    links: List[str] = []
    with open('files/links.txt', mode='r', encoding="utf-8") as file_links:
        with open('files/index.txt', mode='w', encoding="utf-8") as file_index:
            for i, link in enumerate(file_links):
                link = link.split('(')[1][:-2]
                links.append(link)
                file_index.write(f'{i}, {link}\n')

    await asyncio.gather(*[parse(link, i) for i, link in enumerate(links)])


if __name__ == '__main__':
    asyncio.run(main())
