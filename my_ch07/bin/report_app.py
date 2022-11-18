import requests


def main():
    choice = input("[R]eport weather or [s]ee reports? ")

    while choice:
        match choice.lower().strip():
            case "r":
                report_event()
            case "s":
                see_events()
            case other:
                print(f"Don't know what to do with {choice}")

        choice = input("[R]eport weather or [s]ee reports? ")


def report_event():
    desc = input("What is happening? ")
    city = input("What city? ")

    data = {
        "description": desc,
        "location": {"city": city},
    }
    url = "http://localhost:8000/api/reports"
    resp = requests.post(url, json=data)
    resp.raise_for_status()

    result = resp.json()
    print(f"Reported new event: {result.get('id')}")


def see_events():
    url = "http://localhost:8000/api/reports"
    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()

    for r in data:
        print(f"{r.get('location').get('city')} has {r.get('description')}")


if __name__ == "__main__":
    main()
