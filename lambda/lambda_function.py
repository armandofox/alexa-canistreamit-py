"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""

from ask import alexa
from canistreamit import search, streaming, rental, purchase, dvd, xfinity

RENTAL_SOURCES = ['vudu_rental', 'apple_itunes_rental', 'youtube_rental']
STREAMING_SOURCES = ['hulu_movies', 'netflix_instant']

def lambda_handler(request_obj, context=None):
    '''
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {}
    return alexa.route_request(request_obj, metadata)

@alexa.intent_handler("SearchIntent")
def search_intent_handler(request):
    title = request.slots['Movie']
    res = results_for(title)
    if not res:
        card = alexa.create_card(title="CanIStreamIt", subtitle="No match", content="No match for " + title)
        return alexa.create_response("I couldn't find a match for that movie name.", end_session=True, card_obj=card)

    if 'streams' in res:
        msg = "can be streamed from " + ", or ".join(res['streams'])
    elif 'rentals' in  res:
        msg = "cannot be streamed, but can be rented " + ", or ".join(res['rentals'])
    else:
        msg = "is only available for purchase"

    msg = title + " " + msg

    card = alexa.create_card(title="CanIStreamIt", subtitle="Results", content="Looked up " + title)

    return(alexa.create_response(msg, card_obj=card, end_session=True))

def results_for(title):
    res = search(title)
    if not res:
        return(False)
    match = res[0]['_id']
    streams = get_streams(match)
    if (streams):
        return({'streams': streams})
    
    rentals = get_rentals(match)
    if (rentals):
        return({'rentals': rentals})

    purchases = get_purchases(match)
    if (purchases):
        return({'purchases': purchases})

    return({})

def get_purchases(id):
    return({})

def get_streams(id):
    res = streaming(id)
    fmt = lambda v: "from {}".format(v['friendlyName'])
    if not res:
        return []
    return [ fmt(v) for (k,v) in res.items() if k in STREAMING_SOURCES ]

# For each key in 'rental', get its friendlyName field stripping out "Rental",
#  and its price converting the dec point to space ("2.99" => "2 99")
def get_rentals(id):
    res = rental(id)
    if not res:
        return []
    fmt = lambda v: "from {} for {}".format(v['friendlyName'].replace(' Rental', ''), str(v['price']).replace('.', ' '))
    return [ fmt(v) for (k,v) in res.items() if k in RENTAL_SOURCES ]


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="CanIStreamIt launched")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="CanIStreamIt signoff")
    

