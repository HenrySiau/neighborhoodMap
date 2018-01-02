from flask import Flask, render_template, jsonify, abort
from urllib.parse import quote
import requests

# import time

app = Flask(__name__)

# ***********
# ********
#  put yelp API Key here

API_KEY = 'YOURYELPAPIKEY'


#  ********
# ***********

@app.route('/')
def index():
    return render_template('index.html')


# here we just use dummy data, in production we need to use a data base.

@app.route('/places/json')
def places_json():
    locations = [
        {'title': 'Tazaki Sushi', "location": {"lat": 37.76095230000001, "lng": -122.4988951},
         'placeID': 'ChIJk4fK65uHhYARhukr5FOLZyk', 'businessID': 'tazaki-sushi-san-francisco',
         'description': "Dont be fooled as you enter Tazaki. It might seem like a small place but it welcomes you with its cozy interior. Very friendly staff made for quick and polite service. They were very helpful in helping select items from the menu. What I liked best about this place is that they put a very thin layer of rice and alot of fish."},
        {'title': 'Urban Curry', "location": {"lat": 37.7978359, "lng": -122.4059645},
         'placeID': 'ChIJDbh0YfSAhYAREaN_pB50ZTA', 'businessID': 'urban-curry-restaurant-san-francisco',
         'description': "Best And only one Authentic Food in San Francisco. Restautant Owner, Mr.Purna Sherpa, who has done an Everest Summit, is very friendly. It's a must go place if you are in city. Don't Miss, Chicken momo, chicken chowmen and most importantly lamb Chhoyla."},
        {'title': 'Club Deluxe', "location": {"lat": 37.76976860000001, "lng": -122.4471395},
         'placeID': 'ChIJhYOzNlOHhYARVUmuI-zEbbk', 'businessID': 'club-deluxe-san-francisco',
         'description': "Club Deluxe is the coolest!   It's right at the corner of Haight and Ashbury, so the place oozes with authentic happy hippie vibes. Good jazz and ecclectic opening acts along with solid cocktails and beer. The salty dog with fresh squeezed grapefruit juice is a go to. This is a cash only establishment so don't forget to being real money. "},
        {'title': 'Cat Club', "location": {"lat": 37.77553839999999, "lng": -122.409834},
         'placeID': 'ChIJ5XC6h4KAhYARr8Mz6VHO1Ps', 'businessID': 'cat-club-san-francisco',
         'description': " It is not pretentious. Dressing the way you feel good does not get the snide looks one might receive at your trendy who is who clubs!  They have great music.  There is not a bunch of twenty year old kids running around!  The variety of people and music makes this place a perfect fit for SF and Me!  People are really social and fun here."},
        {'title': 'Wonderland SF Gallery & Boutique', "location": {"lat": 37.7539827802915, "lng": -122.4195797197085},
         'placeID': 'ChIJvZcjfj9-j4ARyLGmh8fyyvk', 'businessID': 'wonderland-sf-gallery-and-boutique-san-francisco-2',
         'description': "Fantastic little boutique by 24th and Valencia in the mission. Really great assortment of everything from T-shirts to high-end art to clothing and lots of other stuff in between. Found these guys extremely friendly and accommodating - you can give me advice for family Christmas gifts."},
        {'title': 'San Francisco Museum of Modern Art', "location": {"lat": 37.7857182, "lng": -122.4010508},
         'placeID': 'ChIJ53I1Yn2AhYAR_Vl1vNygfMg', 'businessID': 'san-francisco-museum-of-modern-art-san-francisco-6',
         'description': "The selection of exhibits are always amazing and innovative. Currently, I love their soundtracks exhibit (closing January 2018). It is mind blowing to see and experience the creativity of these artists. This exhibit is also nicely interactive! 7 floors is a lot of cover in one day. I would tend to stick to 2-3 floors per visit so that you don't get museum'd out. Maybe have a nice lunch then see another floor, if you are up to it. The food is really quite good but it is expensive. There is also a lovely Sightglass coffee location on the 3rd floor."}
    ]
    # time.sleep(3) # test server side delay
    return jsonify(locations)


@app.route('/filter/<catalog>/json')
def catalog_json(catalog):
    catalogs = ('restaurants', 'clubs', 'arts')
    locations = {
        'restaurants': [
            {'title': 'Tazaki Sushi', "location": {"lat": 37.76095230000001, "lng": -122.4988951},
             'placeID': 'ChIJk4fK65uHhYARhukr5FOLZyk', 'businessID': 'tazaki-sushi-san-francisco',
             'description': "Dont be fooled as you enter Tazaki. It might seem like a small place but it welcomes you with its cozy interior. Very friendly staff made for quick and polite service. They were very helpful in helping select items from the menu. What I liked best about this place is that they put a very thin layer of rice and alot of fish."},
            {'title': 'Urban Curry', "location": {"lat": 37.7978359, "lng": -122.4059645},
             'placeID': 'ChIJDbh0YfSAhYAREaN_pB50ZTA', 'businessID': 'urban-curry-restaurant-san-francisco',
             'description': "Best And only one Authentic Food in San Francisco. Restautant Owner, Mr.Purna Sherpa, who has done an Everest Summit, is very friendly. It's a must go place if you are in city. Don't Miss, Chicken momo, chicken chowmen and most importantly lamb Chhoyla."},
        ],
        'clubs': [
            {'title': 'Club Deluxe', "location": {"lat": 37.76976860000001, "lng": -122.4471395},
             'placeID': 'ChIJhYOzNlOHhYARVUmuI-zEbbk', 'businessID': 'club-deluxe-san-francisco',
             'description': "Club Deluxe is the coolest!   It's right at the corner of Haight and Ashbury, so the place oozes with authentic happy hippie vibes. Good jazz and ecclectic opening acts along with solid cocktails and beer. The salty dog with fresh squeezed grapefruit juice is a go to. This is a cash only establishment so don't forget to being real money. "},
            {'title': 'Cat Club', "location": {"lat": 37.77553839999999, "lng": -122.409834},
             'placeID': 'ChIJ5XC6h4KAhYARr8Mz6VHO1Ps', 'businessID': 'cat-club-san-francisco',
             'description': " It is not pretentious. Dressing the way you feel good does not get the snide looks one might receive at your trendy who is who clubs!  They have great music.  There is not a bunch of twenty year old kids running around!  The variety of people and music makes this place a perfect fit for SF and Me!  People are really social and fun here."}
        ],
        'arts': [
            {'title': 'Wonderland SF Gallery & Boutique',
             "location": {"lat": 37.7539827802915, "lng": -122.4195797197085},
             'placeID': 'ChIJvZcjfj9-j4ARyLGmh8fyyvk',
             'businessID': 'wonderland-sf-gallery-and-boutique-san-francisco-2',
             'description': "Fantastic little boutique by 24th and Valencia in the mission. Really great assortment of everything from T-shirts to high-end art to clothing and lots of other stuff in between. Found these guys extremely friendly and accommodating - you can give me advice for family Christmas gifts."},
            {'title': 'San Francisco Museum of Modern Art', "location": {"lat": 37.7857182, "lng": -122.4010508},
             'placeID': 'ChIJ53I1Yn2AhYAR_Vl1vNygfMg',
             'businessID': 'san-francisco-museum-of-modern-art-san-francisco-6',
             'description': "The selection of exhibits are always amazing and innovative. Currently, I love their soundtracks exhibit (closing January 2018). It is mind blowing to see and experience the creativity of these artists. This exhibit is also nicely interactive! 7 floors is a lot of cover in one day. I would tend to stick to 2-3 floors per visit so that you don't get museum'd out. Maybe have a nice lunch then see another floor, if you are up to it. The food is really quite good but it is expensive. There is also a lovely Sightglass coffee location on the 3rd floor."}
        ]
    }
    if catalog in catalogs:
        return jsonify(locations[catalog])
    else:
        return "{} does not exist!".format(catalog)


# fetch data from Yelp and return as a json object
@app.route('/yelp/<business_id>/json')
def get_yelp_data(business_id):
    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    BUSINESS_PATH = '/v3/businesses/'

    business_path = BUSINESS_PATH + business_id
    url = '{0}{1}'.format(API_HOST, quote(business_path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer {}'.format(API_KEY),
    }
    response = requests.request('GET', url, headers=headers, params=None)
    if response.status_code == 200:
        return jsonify(response.json())
    if response.status_code == 404:
        return abort(404)
    else:
        return abort(500)


@app.route('/places2/json')
def places_json2():
    locations = {
        'restaurants': [
            {'title': 'Tazaki Sushi', "location": {"lat": 37.76095230000001, "lng": -122.4988951},
             'placeID': 'ChIJk4fK65uHhYARhukr5FOLZyk', 'businessID': 'tazaki-sushi-san-francisco',
             'description': "Dont be fooled as you enter Tazaki. It might seem like a small place but it welcomes you with its cozy interior. Very friendly staff made for quick and polite service. They were very helpful in helping select items from the menu. What I liked best about this place is that they put a very thin layer of rice and alot of fish."},
            {'title': 'Urban Curry', "location": {"lat": 37.7978359, "lng": -122.4059645},
             'placeID': 'ChIJDbh0YfSAhYAREaN_pB50ZTA', 'businessID': 'urban-curry-restaurant-san-francisco',
             'description': "Best And only one Authentic Food in San Francisco. Restautant Owner, Mr.Purna Sherpa, who has done an Everest Summit, is very friendly. It's a must go place if you are in city. Don't Miss, Chicken momo, chicken chowmen and most importantly lamb Chhoyla."},
        ],
        'clubs': [
            {'title': 'Club Deluxe', "location": {"lat": 37.76976860000001, "lng": -122.4471395},
             'placeID': 'ChIJhYOzNlOHhYARVUmuI-zEbbk', 'businessID': 'club-deluxe-san-francisco',
             'description': "Club Deluxe is the coolest!   It's right at the corner of Haight and Ashbury, so the place oozes with authentic happy hippie vibes. Good jazz and ecclectic opening acts along with solid cocktails and beer. The salty dog with fresh squeezed grapefruit juice is a go to. This is a cash only establishment so don't forget to being real money. "},
            {'title': 'Cat Club', "location": {"lat": 37.77553839999999, "lng": -122.409834},
             'placeID': 'ChIJ5XC6h4KAhYARr8Mz6VHO1Ps', 'businessID': 'cat-club-san-francisco',
             'description': " It is not pretentious. Dressing the way you feel good does not get the snide looks one might receive at your trendy who is who clubs!  They have great music.  There is not a bunch of twenty year old kids running around!  The variety of people and music makes this place a perfect fit for SF and Me!  People are really social and fun here."}
        ],
        'arts': [
            {'title': 'Wonderland SF Gallery & Boutique',
             "location": {"lat": 37.7539827802915, "lng": -122.4195797197085},
             'placeID': 'ChIJvZcjfj9-j4ARyLGmh8fyyvk',
             'businessID': 'wonderland-sf-gallery-and-boutique-san-francisco-2',
             'description': "Fantastic little boutique by 24th and Valencia in the mission. Really great assortment of everything from T-shirts to high-end art to clothing and lots of other stuff in between. Found these guys extremely friendly and accommodating - you can give me advice for family Christmas gifts."},
            {'title': 'San Francisco Museum of Modern Art', "location": {"lat": 37.7857182, "lng": -122.4010508},
             'placeID': 'ChIJ53I1Yn2AhYAR_Vl1vNygfMg',
             'businessID': 'san-francisco-museum-of-modern-art-san-francisco-6',
             'description': "The selection of exhibits are always amazing and innovative. Currently, I love their soundtracks exhibit (closing January 2018). It is mind blowing to see and experience the creativity of these artists. This exhibit is also nicely interactive! 7 floors is a lot of cover in one day. I would tend to stick to 2-3 floors per visit so that you don't get museum'd out. Maybe have a nice lunch then see another floor, if you are up to it. The food is really quite good but it is expensive. There is also a lovely Sightglass coffee location on the 3rd floor."}
        ]
    }
    # time.sleep(3) # test server side delay
    return jsonify(locations)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(port=8000)
