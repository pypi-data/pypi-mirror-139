import requests
from requests_html import HTMLSession
welcome = '''
simpleip by Kia#0927
Note: You NEED a secure & fast internet connection for this to work.
''' # Welcome message (DONT DELETE)
print(welcome) # Shows welcome message (DONT DELETE)
url = "https://kiaschest.com/api/ip/get_current_ip" # Kia's PHP api method
url2 = "https://ip-api.com/json" # IP-API's JSON returning api method
def get_client_ip():
    try:
        session = HTMLSession()
        response = session.get(url)
        ip = response.html.find('p')
        return ip[0].text
    except Exception as e:
        alternate = requests.get(url2).json()['query']
        return alternate
