import requests
def detect_item(image,key):
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/530debd0-f73d-476c-9fce-552b8841fd03/LabelFile/'
    data = {'file': open(image, 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(key, ''), files=data)
    return (response.text)