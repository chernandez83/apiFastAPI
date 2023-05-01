from urllib import request

URL = 'http://localhost/'

response = request.urlopen(URL)
print(response.read())