import requests


# url = "http://localhost:8000/posts/"
# headers = {
#     "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwiZXhwIjoxNzAxMDU1OTI1fQ.60ObFL1dsjKCOdejO1XT5cAkNP0X28x3TiOn_qQYX0Q",
#     "Content-Type": "application/json",
# }
# data = {"title": "Example Title", "content": "Example Content", "published": True}

# response = requests.post(url, headers=headers, json=data)

url = 'http://localhost:8000/login/'
email = "ukas@gmail.com"
password = "ukas123"
data = {"email":email, "password":password}
req = requests.post(url, data)
print(req.status_code)


