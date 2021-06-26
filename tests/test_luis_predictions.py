from luis_query import predict_query
import json

utterances = {"None": "i'd like to rent a car", 
        "Greetings": "Good morning",
        "GetWeather": "what's the weather forecast?", 
        "BookFlight": "Book me a flight from Paris to Munich from July 31 to August 31 for a budget of 800$"}

def test_luis_prediction_none_intent():
    response = predict_query(utterances["None"])
    assert response["prediction"]["topIntent"] == "None"


def test_luis_prediction_greetings_intent():
    response = predict_query(utterances["Greetings"])
    assert response["prediction"]["topIntent"] == "Greetings"

    
def test_luis_prediction_getweather_intent():
    response = predict_query(utterances["GetWeather"])
    assert response["prediction"]["topIntent"] == "GetWeather"


def test_luis_prediction_bookflight_intent():
    response = predict_query(utterances["BookFlight"])
    assert response["prediction"]["topIntent"] == "BookFlight"
    assert response["prediction"]["entities"]["$instance"]["From"][0]["text"] == "Paris"
    assert response["prediction"]["entities"]["$instance"]["To"][0]["text"] == "Munich"
    assert response["prediction"]["entities"]["$instance"]["Departure"][0]["text"] == "July 31"
    assert response["prediction"]["entities"]["$instance"]["Return"][0]["text"] == "August 31"
    assert response["prediction"]["entities"]["$instance"]["Budget"][0]["text"] == "800$"


    

