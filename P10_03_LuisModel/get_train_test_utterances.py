##################################################################################################
# This script is used to create train/test sets json files used to train and validate LUIS model #
##################################################################################################

import argparse
import time
import os
import json


def open_file(path_to_file):
    with open(path_to_file) as json_file:
        file = json.load(json_file)
    
    return file


def get_bookflight_utterances(path_to_file):
    labeledExampleUtteranceBookFlightIntent = []
    
    data = open_file(path_to_file)
    for i in range(len(data)):
        utterance = {}
        request = data[i]["turns"][0]
        TEXT = request["text"]
        info = request["labels"]["frames"][0]["info"]
        
        if len(info) > 0 and TEXT:
        
            utterance["text"] = TEXT
            utterance["intentName"] = "BookFlight"
            utterance["entityLabels"] = []
            
            if "or_city" in info.keys():
                for j in range(len(request["labels"]["acts"])):
                    for result in request["labels"]["acts"][j]["args"]:
                        if result["key"] == "or_city": 
                            OR_CITY = result["val"]
                            if TEXT.find(OR_CITY) != -1:
                                OR_CITY_START_POS = TEXT.find(OR_CITY)
                                OR_CITY_END_POS = TEXT.find(OR_CITY) + (len(OR_CITY) - 1)
                                utterance["entityLabels"].append({"startCharIndex": OR_CITY_START_POS,
                                                                "endCharIndex": OR_CITY_END_POS,
                                                                "entityName": "From"})#,
                                                                #"children": [{"startCharIndex": OR_CITY_START_POS,
                                                                #            "endCharIndex": OR_CITY_END_POS,
                                                                #            "entityName": "Airport"}]})
                            
            if "dst_city" in info.keys():
                for j in range(len(request["labels"]["acts"])):
                    for result in request["labels"]["acts"][j]["args"]:
                        if result["key"] == "dst_city": 
                            DST_CITY = result["val"]
                            if TEXT.find(DST_CITY) != -1:
                                DST_CITY_START_POS = TEXT.find(DST_CITY)
                                DST_CITY_END_POS = TEXT.find(DST_CITY) + (len(DST_CITY) - 1)
                                utterance["entityLabels"].append({"startCharIndex": DST_CITY_START_POS,
                                                                "endCharIndex": DST_CITY_END_POS,
                                                                "entityName": "To"})#,
                                                                #"children": [{"startCharIndex": DST_CITY_START_POS,
                                                                #            "endCharIndex": DST_CITY_END_POS,
                                                                #            "entityName": "Airport"}]})
                                
            if "str_date" in info.keys():
                for j in range(len(request["labels"]["acts"])):
                    for result in request["labels"]["acts"][j]["args"]:
                        if result["key"] == "str_date": 
                            STR_DATE = result["val"]
                            if TEXT.find(STR_DATE) != -1:
                                STR_DATE_START_POS = TEXT.find(STR_DATE)
                                STR_DATE_END_POS = TEXT.find(STR_DATE) + (len(STR_DATE) - 1)
                                utterance["entityLabels"].append({"startCharIndex": STR_DATE_START_POS,
                                                                "endCharIndex": STR_DATE_END_POS,
                                                                "entityName": "Departure"})#,
                                                                #"children": []})
                                
            if "end_date" in info.keys():
                for j in range(len(request["labels"]["acts"])):
                    for result in request["labels"]["acts"][j]["args"]:
                        if result["key"] == "end_date": 
                            END_DATE = result["val"]
                            if TEXT.find(END_DATE) != -1:
                                END_DATE_START_POS = TEXT.find(END_DATE)
                                END_DATE_END_POS = TEXT.find(END_DATE) + (len(END_DATE) - 1)
                                utterance["entityLabels"].append({"startCharIndex": END_DATE_START_POS,
                                                                "endCharIndex": END_DATE_END_POS,
                                                                "entityName": "Return"})#,
                                                                #"children": []})

            if "budget" in info.keys():
                for j in range(len(request["labels"]["acts"])):
                    for result in request["labels"]["acts"][j]["args"]:
                        if result["key"] == "budget": 
                            BUDGET = result["val"]
                            if TEXT.find(BUDGET) != -1:
                                BUDGET_START_POS = TEXT.find(BUDGET)
                                BUDGET_END_POS = TEXT.find(BUDGET) + (len(BUDGET) - 1)
                                utterance["entityLabels"].append({"startCharIndex": BUDGET_START_POS,
                                                                "endCharIndex": BUDGET_END_POS,
                                                                "entityName": "Budget"})#,
                                                                #"children": []})            


            labeledExampleUtteranceBookFlightIntent.append(utterance)
    
    return labeledExampleUtteranceBookFlightIntent


def get_other_utterances():
    # Define labeled examples (Intent = Greetings)    
    labeledExampleUtteranceGreetingsIntent = [
        {"text": "Hello",
         "intentName": "Greetings"},
        {"text": "Good morning",
         "intentName": "Greetings"},
        {"text": "Good afternoon",
         "intentName": "Greetings"},
        {"text": "How are you?",
         "intentName": "Greetings"},
        {"text": "Hi there",
         "intentName": "Greetings"},
        {"text": "Helloooooo",
         "intentName": "Greetings"},
        {"text": "Hey",
         "intentName": "Greetings"},
        {"text": "Hallo",
         "intentName": "Greetings"},
        {"text": "Hi",
         "intentName": "Greetings"},
        {"text": "Hey here",
         "intentName": "Greetings"}         
    ]


    # Define labeled examples (Intent = GetWeather)
    labeledExampleUtteranceGetWeatherIntent = [
        {"text": "what's the forecast for this friday?",
         "intentName": "GetWeather"},
        {"text": "what's the weather like for tomorrow",
         "intentName": "GetWeather"},
        {"text": "what's the weather like in new york",
         "intentName": "GetWeather"},    
        {"text": "what's the weather like?",
         "intentName": "GetWeather"},
        {"text": "what's the weather forecast?",
         "intentName": "GetWeather"}         
    ]

    # Define labeled examples (Intent = None)
    labeledExampleUtteranceNoneIntent = [
        {"text": "winter is coming",
         "intentName": "None"},
        {"text": "i'd like to rent a car",
         "intentName": "None"},         
        {"text": "book a hotel in new york",
         "intentName": "None"},
        {"text": "find an airport near me",
         "intentName": "None"},
        {"text": "book a restaurant",
         "intentName": "None"}
    ]    

    return (labeledExampleUtteranceGreetingsIntent, labeledExampleUtteranceGetWeatherIntent,
    labeledExampleUtteranceNoneIntent)



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--path_to_file", type=str, default="./frames.json",
                        help="Path to the file with data to extract")
    parser.add_argument("--test_split_ratio", type=float, default=0.2,
                        help="Ratio of data to put in the test set")
    parser.add_argument("--path_to_save_folder", type=str, default="./",
                        help="Folder to save train and test json files with utterances and intents")                        


    args = parser.parse_args()
    
    try:
        os.makedirs(args.path_to_save_folder, exist_ok=True)
    except OSError as error:
        print("Save folder could not be created")

    if not os.path.isfile(args.path_to_file):
        print("Path to file with data to extract not found")
        return
        
    print("Path to the file with data to extract:", args.path_to_file)
    
    
    labeledExampleUtteranceBookFlightIntent = get_bookflight_utterances(args.path_to_file)
    
    BookFlightUtterancesTrainSet = []
    BookFlightUtterancesTestSet = []
    for i in range(0, int(args.test_split_ratio * len(labeledExampleUtteranceBookFlightIntent))):
        BookFlightUtterancesTestSet.append(labeledExampleUtteranceBookFlightIntent[i])
    for j in range(int(args.test_split_ratio * len(labeledExampleUtteranceBookFlightIntent)), 
                   len(labeledExampleUtteranceBookFlightIntent)):
        BookFlightUtterancesTrainSet.append(labeledExampleUtteranceBookFlightIntent[j])

    
    (labeledExampleUtteranceGreetingsIntent, labeledExampleUtteranceGetWeatherIntent,
    labeledExampleUtteranceNoneIntent) = get_other_utterances()
        
    utterances = [labeledExampleUtteranceGreetingsIntent, labeledExampleUtteranceGetWeatherIntent, 
    labeledExampleUtteranceNoneIntent]
                  
    OtherUtterancesTrainSet = []
    OtherUtterancesTestSet = []
    for utterance in utterances:
        for i in range(0, int(args.test_split_ratio * len(utterance))):
            OtherUtterancesTestSet.append(utterance[i]) 
        for j in range(int(args.test_split_ratio * len(utterance)), len(utterance)):
            OtherUtterancesTrainSet.append(utterance[j])
    
    with open(os.path.join(args.path_to_save_folder, "trainset.json"), "w") as write_file:
        json.dump({"BookFlightUtterances": BookFlightUtterancesTrainSet, 
                   "OtherUtterances": OtherUtterancesTrainSet}, write_file)
    
    with open(os.path.join(args.path_to_save_folder, "testset.json"), "w") as write_file:
        json.dump({"BookFlightUtterances": BookFlightUtterancesTestSet, 
                   "OtherUtterances": OtherUtterancesTestSet}, write_file)

if __name__ == "__main__":
    
    start_time = time.time()
    main()
    time_elapsed = time.time() - start_time
    
    print("\n------------")
    print("Total used time: {:.0f}m {:.0f}s".format(time_elapsed // 60, time_elapsed % 60))
