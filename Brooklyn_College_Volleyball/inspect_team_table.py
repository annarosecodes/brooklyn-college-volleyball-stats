import requests
from bs4 import BeautifulSoup

url = "https://www.brooklyncollegeathletics.com/sports/mens-volleyball/stats/2024"

response = requests.get(url, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find_all("table")[0]

for row in table.find_all("tr"):
    cells = [
        cell.get_text(" ", strip=True)
        for cell in row.find_all(["th", "td"])
    ]
    print(cells)