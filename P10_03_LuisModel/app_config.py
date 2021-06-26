#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ App Configuration """

    AUTHORING_KEY = os.environ.get("authoringKey", "28a2386f09ba4c15b42305750f8d75ef")
    AUTHORING_ENDPOINT = os.environ.get("authoringEndpoint", 
                                        "https://p10-luismodel-authoring.cognitiveservices.azure.com/")
    PREDICTION_KEY = os.environ.get("predictionKey", "de385d52403447e0b0d9ba5783c13054")
    PREDICTION_ENDPOINT = os.environ.get("predictionEndpoint", 
                                        "https://p10-luismodel.cognitiveservices.azure.com/")
    LUIS_APP_ID = os.environ.get("LuisAppId", "3112d8b1-7741-4027-a8f0-fac071622c68")                                        
