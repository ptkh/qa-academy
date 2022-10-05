from framework.utils.random_util import RandomUtil


class TestData:
    ID = 'id'
    POSTS = 'posts'
    USERS = 'users'

    post = {
                'userId': 1,
                'title': RandomUtil.get_string(20),
                'body': RandomUtil.get_string(100)
            }
    existent_post_id = 99
    existent_post_user_id = 10
    absent_post_id = 150
    user_id = 5
    user = {
        'name': 'Chelsey Dietrich',
        'username': 'Kamren',
        'email': 'Lucio_Hettinger@annie.ca',
        'address': {
                        'street': 'Skiles Walks',
                        'suite': 'Suite 351',
                        'city': 'Roscoeview',
                        'zipcode': '33263',
                        'geo': {
                                'lat': '-31.8129',
                                'lng': '62.5342'
                        }
        },
        'phone': '(254)954-1289',
        'website': 'demarco.info',
        'company': {
                        'name': 'Keebler LLC',
                        'catchPhrase': 'User-centric fault-tolerant solution',
                        'bs': 'revolutionize end-to-end systems',
        }
    }
