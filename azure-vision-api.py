"""
Call the Azure AI Vision 3.2 GA Read API

https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/how-to/call-read-api

also

https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/
    client-library?tabs=windows%2Cvisual-studio&pivots=programming-language-python
17 October 2023

----------------------------------------------------------
How to create and launch Python Virtual environment in VS Code

problem: Neither python nor pip are recognized in the terminal 
    e.g. python --version 
    does not work

1) So...Create a virtual environment
    Manage > Command prompt... Python Create Enviroment

    This appears to work because the .venv folder appears 
        - but python and pip are still unknown in the terminal

2) So...Activate the virtual environment
    In the terminal, navigate to the folder (probably the project folder) 
    that contains the .venv folder

    In the terminal .venv\Scripts\activate

    A green (.venv) should appear to the left of the Terminal prompt
    if the virtual environment is working.
----------------------------------------------------------

Run Vision application from terminal with
python azure-vision-api.py

The SDK

"""
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
print("===== Read File - remote =====")
# Get an image with text
# localhost does not work

read_image_url = "https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png"

# Call API with URL and raw response (allows you to get the operation location)

"""
Optional read Parameters

language
Default: the service extracts all text from your images or documents including mixed languages.
see: https://aka.ms/ocr-languages for list of supported languages.
string: "en", "fr", "zn-Hans" etc.

OCR model model-version
Default: "latest"
string: "latest", "2022-04-30" or "2021-04-12"

readingOrder
The algorithm that should be applied when ordering the extract text elements. 
Default: basic
string: "basic" or "natural"

pages
Only useful in multipage TIFF or PDF documents.
Default: all pages
e.g.
"1, 2"  page 1 and 2
"2-5"   pages 2 to 5
"5-"    page 5 onwards
"-10"   pages 1 to 10
You can mix all these together and ranges are allowed to overlap without redundant processing taking place.
The service will accept the request if it can process at least one page of the document.
"""
read_response = computervision_client.read(read_image_url,  raw=True)

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]

# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results 
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()
'''
END - Read File - remote
'''

print("End of Computer Vision quickstart.")















































