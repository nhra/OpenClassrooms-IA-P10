from app_config import DefaultConfig
import requests
import json
import os
import time
import argparse


def open_json_file(path_to_file):
    with open(path_to_file, "r") as json_file:
        file = json.load(json_file)
    
    return file


def predict_query(utterance):
    try:

        # YOUR-APP-ID: The App ID GUID found on the www.luis.ai Application Settings page.
        appId = DefaultConfig.LUIS_APP_ID

        # YOUR-PREDICTION-KEY: Your LUIS prediction key, 32 character value.
        prediction_key = DefaultConfig.AUTHORING_KEY

        # YOUR-PREDICTION-ENDPOINT: Replace with your prediction endpoint.
        # For example, "https://westus.api.cognitive.microsoft.com/"
        prediction_endpoint = DefaultConfig.PREDICTION_ENDPOINT

        # The headers to use in this REST call.
        headers = {
        }

        # The URL parameters to use in this REST call.
        params ={
            'query': utterance,
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': prediction_key
        }


        # Make the REST call.
        response = requests.get(f'{prediction_endpoint}luis/prediction/v3.0/apps/{appId}/slots/production/predict', headers=headers, params=params)

        # Display the results on the console.
        return response.json()


    except Exception as e:
        # Display the error string.
        print(f'{e}')


def str_to_bool(s):
    if s == "True":
         return True
    elif s == "False":
         return False
    else:
         raise ValueError

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--path_to_json_file", type=str, default="./testset_small.json",
                        help="Path to the test JSON file with data to extract")
    parser.add_argument("--save_results", type=str, default="False", choices=["True", "False"],
                        help="Folder to save JSON result file")
    parser.add_argument("--path_to_save_folder", type=str, default="./",
                        help="Folder to save JSON result file")


    args = parser.parse_args()

    try:
        os.makedirs(args.path_to_save_folder, exist_ok=True)
    except OSError as error:
        print("Save folder could not be created")

    if not os.path.isfile(args.path_to_json_file):
        print("Path to the test JSON file with data to extract not found")
        return    

    print("Path to the file with data to extract:", args.path_to_json_file)

    gt_vs_pr = {"results": [], "accuracy": 0.0}
    n = 0
    acc = 0

    utterances = open_json_file(args.path_to_json_file)

    for utterance in utterances["BookFlightUtterances"]:
        TEXT = utterance["text"]
        GT_INTENT = utterance["intentName"]
        GT_ENTITIES = utterance["entityLabels"]

        GT_FROM = None
        GT_TO = None
        GT_DEPARTURE = None
        GT_RETURN = None
        GT_BUDGET = None
        
        for entity in utterance["entityLabels"]:
            if entity["entityName"] == "From":
                GT_FROM = TEXT[entity["startCharIndex"]:(entity["endCharIndex"]+1)] 
            if entity["entityName"] == "To":
                GT_TO = TEXT[entity["startCharIndex"]:(entity["endCharIndex"]+1)]
            if entity["entityName"] == "Departure":
                GT_DEPARTURE = TEXT[entity["startCharIndex"]:(entity["endCharIndex"]+1)]
            if entity["entityName"] == "Return":
                GT_RETURN = TEXT[entity["startCharIndex"]:(entity["endCharIndex"]+1)]
            if entity["entityName"] == "Budget":
                GT_BUDGET = TEXT[entity["startCharIndex"]:(entity["endCharIndex"]+1)]

        PR_FROM = None
        PR_TO = None
        PR_DEPARTURE = None
        PR_RETURN = None
        PR_BUDGET = None

        RESPONSE = predict_query(TEXT)
        PR_INTENT = RESPONSE["prediction"]["topIntent"]
        entities = RESPONSE["prediction"]["entities"]
        if "From" in entities:
            PR_FROM = entities["From"][0]
        if "To" in entities:
            PR_TO = entities["To"][0]
        if "Departure" in entities:
            PR_DEPARTURE = entities["Departure"][0]
        if "Return" in entities:
            PR_RETURN = entities["Return"][0]
        if "Budget" in entities:
            PR_BUDGET = entities["Budget"][0]

        ACCURACY = int(GT_INTENT == PR_INTENT) + int(GT_FROM == PR_FROM)
        ACCURACY = ACCURACY + int(GT_TO == PR_TO) + int(GT_DEPARTURE == PR_DEPARTURE) 
        ACCURACY = ACCURACY + int(GT_RETURN == PR_RETURN) + int(GT_BUDGET == PR_BUDGET)
        ACCURACY = ACCURACY / 6

        acc += ACCURACY
        n += 1

        gt_vs_pr["results"].append(
            {"Text": TEXT,
            "Intent": {"GT": GT_INTENT, "PR": PR_INTENT}, 
            "From": {"GT": GT_FROM, "PR": PR_FROM},
            "To": {"GT": GT_TO, "PR": PR_TO}, 
            "Departure": {"GT": GT_DEPARTURE, "PR": PR_DEPARTURE}, 
            "Return": {"GT": GT_RETURN, "PR": PR_RETURN}, 
            "Budget": {"GT": GT_BUDGET, "PR": PR_BUDGET}, 
            "Accuracy": round(ACCURACY, 2)
            }
        )

    gt_vs_pr["overall_accuracy"] = round(float(acc / n), 2)
    
    if not str_to_bool(args.save_results):
        #print(gt_vs_pr)
        return gt_vs_pr
    else:
        with open(os.path.join(args.path_to_save_folder, "gt_vs_pr.json"), "w") as write_file:
            json.dump(gt_vs_pr, write_file)    

if __name__ == "__main__":
    
    start_time = time.time()
    main()
    time_elapsed = time.time() - start_time
    
    print("\n------------")
    print("Total used time: {:.0f}m {:.0f}s".format(time_elapsed // 60, time_elapsed % 60))
