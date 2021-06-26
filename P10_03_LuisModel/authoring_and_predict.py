from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.authoring.models import ApplicationCreateObject
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce
from app_config import DefaultConfig

import json, time, uuid


#def get_child_id(modelObject, childName):
#    
#    theseChildren = next(filter((lambda child: child.name == childName), modelObject.children))
#    childId = theseChildren.id
#    
#    return childId


def open_file(path_to_file):
    with open(path_to_file, "r") as json_file:
        file = json.load(json_file)
    
    return file


def quickstart():
    
    print("###########################")
    print("# Create Luis Application #")
    print("###########################")
    
    # Set config
    authoringKey = DefaultConfig.AUTHORING_KEY
    authoringEndpoint = DefaultConfig.AUTHORING_ENDPOINT
    predictionKey = DefaultConfig.PREDICTION_KEY
    predictionEndpoint = DefaultConfig.PREDICTION_ENDPOINT
    
    # Authenticate client
    client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))
    
    # define app basics
    appName = "BookFlight " + str(uuid.uuid4())
    versionId = "0.1"
    culture = "en-us"
    
    appDefinition = ApplicationCreateObject(name=appName, initial_version_id=versionId, culture=culture)

    # create app
    app_id = client.apps.add(appDefinition)

    # get app id - necessary for all other changes
    print("Created LUIS app with ID: {}".format(app_id))
    
    
    print("\n##################")
    print("# Create intents #")
    print("##################")
    
    #intents = ["BookFlight", "GetWeather", "Greetings", "Cancel"]
    
    intents = ["BookFlight", "GetWeather", "Greetings"]
    for intent in intents:
        client.model.add_intent(app_id, versionId, intent)
        print("Created LUIS intent: {}".format(intent))

    # BookFlight
    #client.model.add_intent(app_id, versionId, "BookFlight")

    # Cancel
    #client.model.add_intent(app_id, versionId, "Cancel")

    # GetWeather
    #client.model.add_intent(app_id, versionId, "GetWeather")

    # Greetings
    #client.model.add_intent(app_id, versionId, "Greetings")


    print("\n###################")
    print("# Create entities #")
    print("###################")

    # Add Prebuilt entity
    prebuilt_entities = ["datetimeV2", "geographyV2", "money"]
    client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=prebuilt_entities)
    for prebuilt_entity in prebuilt_entities:
        print("Added prebuilt entity: {}".format(prebuilt_entity))

    # Add machine-learned entities
    #AirportEntityDefinition = {"name": "Airport"}
    name = "From"
    DepartureAirportEntity = client.model.add_entity(app_id, versionId, name=name)#, children=[AirportEntityDefinition])
    print("Added ML entity: {}".format(name))
    
    name = "To"
    DestinationAirportEntity = client.model.add_entity(app_id, versionId, name=name)#, children=[AirportEntityDefinition])
    print("Added ML entity: {}".format(name))
    
    name = "Departure"
    DepartureDateEntity = client.model.add_entity(app_id, versionId, name=name)
    print("Added ML entity: {}".format(name))

    name = "Return"
    ReturnDateEntity = client.model.add_entity(app_id, versionId, name=name)
    print("Added ML entity: {}".format(name))

    name = "Budget"
    BudgetEntity = client.model.add_entity(app_id, versionId, name=name)
    print("Added ML entity: {}".format(name))

    # Get entities and subentities
    #DepartureAirportObject = client.model.get_entity(app_id, versionId, DepartureAirportEntity)
    #DepartureAirportId = get_child_id(DepartureAirportObject, "Airport")
    #DestinationAirportObject = client.model.get_entity(app_id, versionId, DestinationAirportEntity)
    #DestinationAirportId = get_child_id(DestinationAirportObject, "Airport")
    
    # add models as features to entity and subentity models
    prebuiltFeatureNotRequiredDefinition_1 = {"model_name": "geographyV2", "is_required": False}
    client.features.add_entity_feature(app_id, versionId, DepartureAirportEntity, prebuiltFeatureNotRequiredDefinition_1)
    client.features.add_entity_feature(app_id, versionId, DestinationAirportEntity, prebuiltFeatureNotRequiredDefinition_1)
    
    prebuiltFeatureNotRequiredDefinition_2 = {"model_name": "datetimeV2", "is_required": False}
    client.features.add_entity_feature(app_id, versionId, DepartureDateEntity, prebuiltFeatureNotRequiredDefinition_2)
    client.features.add_entity_feature(app_id, versionId, ReturnDateEntity, prebuiltFeatureNotRequiredDefinition_2)
    
    prebuiltFeatureNotRequiredDefinition_3 = {"model_name": "money", "is_required": False}
    client.features.add_entity_feature(app_id, versionId, BudgetEntity, prebuiltFeatureNotRequiredDefinition_3)

    
    print("\n##################")
    print("# Add utterances #")
    print("##################") 

    # Add an example for the entity.
    # Enable nested children to allow using multiple models with the same name.
    utterances = open_file("./trainset.json")
    
    #print("BookFlightUtterances")
    for utterance in utterances["BookFlightUtterances"]:
        #client.examples.add(app_id, versionId, utterance, {"enableNestedChildren": True})
        client.examples.add(app_id, versionId, utterance, {"enableNestedChildren": False})
    print("Added {} BookFlight utterances".format(len(utterances["BookFlightUtterances"])))
    
    #print("OtherUtterances")
    for utterance in utterances["OtherUtterances"]:
        client.examples.add(app_id, versionId, utterance, {"enableNestedChildren": False})
    print("Added {} Other utterances".format(len(utterances["OtherUtterances"])))            

    print("\n###################")
    print("# Train the model #")
    print("###################")

    client.train.train_version(app_id, versionId)
    waiting = True
    while waiting:
        info = client.train.get_status(app_id, versionId)

        # get_status returns a list of training statuses, one for each model. Loop through them and make sure all are done.
        waiting = any(map(lambda x: 'Queued' == x.details.status or 'InProgress' == x.details.status, info))
        if waiting:
            print ("Waiting 10 seconds for training to complete...")
            time.sleep(10)
        else: 
            print ("Model trained")
            waiting = False    
    
    
    print("\n###################")
    print("# Publish the app #")
    print("###################")

    responseEndpointInfo = client.apps.publish(app_id, versionId, is_staging=False)
    print("App published")
    
    print("\n########################")
    print("# Get prediction runtime #")
    print("##########################")    
    
    runtimeCredentials = CognitiveServicesCredentials(authoringKey)
    clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)
    print("Client authenticated")

    query = "Hi, I need to go to Mos Eisley for a wedding, leaving on Saturday, August 13, 2016 \
        and returning on Tuesday, August 16, 2016. Preferably for $3700"

    print("\nText query: {}".format(query))

    # Production == slot name
    predictionRequest = {"query" : query}
    predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
    print("Top intent: {}".format(predictionResponse.prediction.top_intent))    
    print("Entities: {}".format(predictionResponse.prediction.entities))
    

quickstart()
