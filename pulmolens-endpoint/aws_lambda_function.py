import json
import boto3
import base64

# defining my endpoint name.
endpoint_name = "Test-PulmoLens-Classifier"
sagemaker_runtime_client = boto3.client('runtime.sagemaker')

# lambda handler function.
def lambda_handler(event, context):
    print(event)
    
    # get the image from the event (the event comes from the API), and decode it for inferencing.
    image = base64.b64decode(event['image'])
    print(image)
    
    # call function to make response on image.
    return _pulmo_lens(image)

# function to take the image and invoke the endpoint.
def _pulmo_lens(image):
    
    # response.
    response = sagemaker_runtime_client.invoke_endpoint(
        EndpointName = endpoint_name,
        ContentType = "application/x-image",
        Body = image
    )
    
    # result.
    result = response['Body'].read()
    result = json.loads(result)
    print("Curr Result: ", result)
    
    # # sending predicted class.
    # y_pred = 0 if result[0] > result[1] else 1
    
    # sending predicted probability for most probable class.
    # prob_result = result[0] if result[0] > result[1] else result[1]
    
    # return messages.
    normal_str = f"We predict you are normal (have no pneumonia) with a probability of: {result[0]}"
    pneumonic_str = f"We predict you have pneumonia with a probability of: {result[1]}"

    return normal_str + "\n" + pneumonic_str