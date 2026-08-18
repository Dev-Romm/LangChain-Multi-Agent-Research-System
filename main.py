from src.tools.tools import web_search, scrape_url

output = scrape_url.invoke({"url": "https://www.caranddriver.com/features/g28985154/future-cars/"})
print(output)