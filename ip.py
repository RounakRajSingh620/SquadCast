import requests

# Submission URL
submission_url = "https://quest.squadcast.tech/api/RA2111003020213/submit/worded_ip"
answer = "209.100.969.228"  # Your extracted IP address
extension = "js"  # Specify the language used

# Prepare the final submission URL
final_url = f"{submission_url}?answer={answer}&extension={extension}"

# Your code to be submitted
code_to_submit = """
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
            if len(ip_parts) == 4:
                break

    if len(ip_parts) != 4:
        return "IP address not found or incomplete"

    ip_address = ".".join(ip_parts)
    return ip_address

url = "https://quest.squadcast.tech/api/RA2111003020213/worded_ip"
ip_address = extract_ip_address(url)
"""

# Making the POST request with code in the body
response = requests.post(final_url, data=code_to_submit)

# Print the response from the submission
print(response.text)
