import asyncio
import json
import random
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,da;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://www.ellesse.com/mens/all-mens-clothing.list",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": ua.random,
}


async def get_page(session, page, size, data, gender):
    url = f"https://www.ellesse.com/{gender}/all-{gender}-clothing.list?facetFilters=en_ellesse_plg_apparelSize_content%3A{size}&pageNumber={page}"

    async with session.get(url=url, headers=headers) as r:
        r_text = await r.text()
        print(url)
        soup = BeautifulSoup(r_text, "lxml")

        products = soup.find_all(
            "div", {"data-testid": "product-item-wrapper"}
        )
        for product in products:
            cloth_title = product.find(
                "h3", {"data-testid": "productblock-title"}
            ).getText()
            cloth_url = "https://www.ellesse.com" + product.find("a").get(
                "href"
            )
            cloth_price = product.find(
                "div", {"data-testid": "sale-price"}
            ).getText()

            data.append(
                {
                    "title": cloth_title,
                    "link": cloth_url,
                    "price": cloth_price,
                    "size": size,
                }
            )
    print(f"Обработана: {page} страница")
    await asyncio.sleep(random.randint(1, 2))


async def gather_data(size, data, gender):
    url = f"https://www.ellesse.com/{gender}/all-{gender}-clothing.list?facetFilters=en_ellesse_plg_apparelSize_content%3A{size}"
    async with aiohttp.ClientSession() as session:
        r = await session.get(
            url=url,
            headers=headers,
        )

        soup = BeautifulSoup(await r.text(), "lxml")
        tasks = []

        try:
            pages_count = int(
                soup.find(
                    "div",
                    {"data-testid": "select-page-dropdown-options-container"},
                )
                .find_all("li", {"role": "option"})[-1]
                .text
            )
        except:
            pages_count = 1

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(
                get_page(session, page, size, data, gender)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)


async def parse_clothes(size, gender):
    data = []
    await gather_data(size, data, gender)
    with open(f"result_{cur_time}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
