from app_config import DefaultConfig
import requests
import json
import time
import argparse


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


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--utterance", type=str, required=True,
                        help="Text of the utterance")

    args = parser.parse_args()

    utterance = args.utterance
    
    response = predict_query(utterance)

    print(response)


if __name__ == "__main__":

    start_time = time.time()
    main()
    time_elapsed = time.time() - start_time

    print("\n------------")
    print("Total used time: {:.0f}m {:.0f}s".format(time_elapsed // 60, time_elapsed % 60))
