import requests

URL = 'http://127.0.0.1:8000/api/v1/reviews'
HEADERS = {'accept': 'application/json'}

############################################################## GET
# QUERYSET = {'page': 1, 'limit': 3}

# response = requests.get(URL, headers=HEADERS, params=QUERYSET) 

# if response.status_code == 200:
#     # print(response.content, '\n')
#     # print(response.headers)
    
#     if response.headers.get('content-type') == 'application/json':
#         print('Solicitud existosa')
#         reviews = response.json()
#         for review in reviews:
#             print(f"Película: {review['movie']['title']:<20} \tScore: {review['score']:>4} \tReview: {review['review']}")


################################################################### POST
# REVIEW = {
#   'user_id': 1,
#   'movie_id': 5,
#   'review': 'Esta película sí da mello',
#   'score': 5
# }

# response = requests.post(URL, headers=HEADERS, json=REVIEW)

# if response.status_code == 200:
#     print('Reseña creada exitosamente\n')
#     print(response.json())
# else:
#     print(response.content)

################################################################### PUT
# REVIEW_ID = 12
# URL = f'http://127.0.0.1:8000/api/v1/reviews/{REVIEW_ID}'

# REVIEW = {
#   'review': 'Esta película sí da mello (creada con requests)',
#   'score': 5
# }

# response = requests.put(URL, headers=HEADERS, json=REVIEW)

# if response.status_code == 200:
#     print('Reseña actualizada exitosamente\n')
#     print(response.json())
# else:
#     print(response.content)

################################################################### DELETE
# REVIEW_ID = 13
# URL = f'http://127.0.0.1:8000/api/v1/reviews/{REVIEW_ID}'

# response = requests.delete(URL, headers=HEADERS)

# if response.status_code == 200:
#     print('Reseña eliminada exitosamente\n')
#     print(response.json())
# else:
#     print(response.content)

################################################################### LOGIN (cookies)
URL = 'http://127.0.0.1:8000/api/v1/users/'
USER = {
  'username': 'Batman',
  'password': '123'
}

response = requests.post(URL + 'login', headers=HEADERS, json=USER)

if response.status_code == 200:
    print('Usuario autenticado exitosamente\n')
    # print(response.json())
    # print(response.cookies) # RequestsCookieJar
    # print(response.cookies.get_dict())
    username = response.cookies.get_dict().get('user')
    user_id = response.cookies.get_dict().get('user_id')
    print(f'Bienvenido, {username}')
    
    cookies = {'user_id': user_id}
    print('Reseñas:')
    reviews = requests.get(URL + 'reviews', headers=HEADERS, cookies=cookies)
    
    if reviews.status_code == 200:
        for review in reviews.json():
            print(f"Película: {review['movie']['title']:<20} \tScore: {review['score']:>4} \tReview: {review['review']}")
    
else:
    print(response.content)