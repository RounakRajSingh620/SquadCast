import requests


def word_to_number(word):
    number_map = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    return number_map.get(word.lower())


def extract_ip_address(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to retrieve passage"

    words = response.text.split()
    ip_parts = []

    for word in words:
        digit = word_to_number(word)
        if digit is not None:
            ip_parts.append(digit)
            if len(ip_parts) == 12:
                break

    if len(ip_parts) != 12:
        return "IP address not found or incomplete"

    ip_address = ".".join(["".join(ip_parts[i : i + 3]) for i in range(0, 12, 3)])
    return ip_address


url = "https://quest.squadcast.tech/api/RA2111003020213/worded_ip"
ip_address = extract_ip_address(url)
print(f"{ip_address.replace('.','_')}")
