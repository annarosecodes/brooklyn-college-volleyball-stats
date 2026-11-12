import requests

for year in range(2012, 2025):
    url = (
        "https://static.brooklyncollegeathletics.com/"
        f"custompages/mvball/{year}/HTML/teamgbg.htm"
    )

    try:
        response = requests.get(url, timeout=15)
        print(year, "|", response.status_code)
    except requests.RequestException as error:
        print(year, "| ERROR:", error)