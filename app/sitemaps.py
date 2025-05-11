import datetime

import bs4
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Decision, Sitemap, engine

date = datetime.datetime.now().strftime("%Y-%m-%d")

# Scrape Main Sitemap
response = requests.get("https://www.va.gov/sitemap_bva.xml")
response.raise_for_status()
content = response.content.decode("utf-8")

soup = bs4.BeautifulSoup(content, "lxml-xml")
sitemap_index = soup.find("sitemapindex")
elements = sitemap_index.find_all("sitemap")

records = []
for element in elements:
    url = element.find("loc").text
    updated = element.find("lastmod").text

    # skip if not updated

    record = Sitemap(
        url=url,
        updated=updated,
        retrieved=date,
    )
    records.append(record)

with Session(engine) as session:
    session.add_all(records)
    session.commit()

# Scrape Annual Sitemaps
with Session(engine) as session:
    query = select(Sitemap).order_by(Sitemap.id.desc())
    sitemaps = list(session.scalars(query))

for sitemap in sitemaps:
    print(sitemap.url)
    response = requests.get(sitemap.url)
    response.raise_for_status()
    content = response.content.decode("utf-8")
    soup = bs4.BeautifulSoup(content, "lxml-xml")
    url_set = soup.find("urlset")
    elements = url_set.find_all("url")

    records = []
    for element in elements:
        url = element.find("loc").text
        updated = element.find("lastmod").text
        record = Decision(
            url=url,
            updated=updated,
            retrieved=date,
        )
        records.append(record)

    with Session(engine) as session:
        session.add_all(records)
        session.commit()
