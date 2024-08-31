from flask import Flask, request, jsonify, Response
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Initialize the Chrome WebDriver in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_sender_score(ip_address):
    url = f"https://senderscore.org/assess/get-your-score/report/?lookup={ip_address}&authenticated=true"
    driver.get(url)

    try:
        # Wait up to 10 seconds for the score element to be present
        score_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.ss-score__num"))
        )
        score = score_element.text
    except Exception as e:
        print(f"Could not retrieve score for IP {ip_address}: {e}")
        score = "N/A"  # or handle the error as you see fit

    return score

@app.route('/')
def index():
    with open(r'D:\plan\index.html', 'r') as file:
        html_content = file.read()
    return Response(html_content, mimetype='text/html')

@app.route('/get_scores', methods=['POST'])
def get_scores():
    # Get the list of IPs from the frontend
    data = request.json
    ips = data['ips']

    # Dictionary to store the scores
    scores = {}

    # Loop over each IP and get the SenderScore
    for ip in ips:
        ip = ip.strip()  # Remove any leading/trailing spaces
        if ip:  # Skip empty entries
            scores[ip] = get_sender_score(ip)

    # Return the scores as JSON
    return jsonify(scores)

if __name__ == '__main__':
    app.run(debug=True)
