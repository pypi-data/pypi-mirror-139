from pylambdatest.BaseLambdaTest import BaseLambdaTest

class APIGatewayLambdaTest(BaseLambdaTest):
    def __init__(self, context):
        event = {
            'resource' : None,
            'path' : None,
            'httpMethod' : None,
            'requestContext' : None,
            'headers' : None,
            'multiValueHeaders' : None,
            'queryStringParameters' : None,
            'multiValueQueryStringParameters' : None,
            'pathParameters' : None,
            'stageVariables' : None,
            'body' : None,
            'isBase64Encoded' : False
        }
        super().__init__(context, event = event)

    def add_event_value(self, key, value):
        if key not in list(self.event.keys()):
            raise Exception('''
                Invalid event value: API Gateway Event only supports the following event values:
                resource, path, httpMethod, requestContext, headers, multiValueHeaders,
                queryStringParameters, multiValueQueryStringParameters, pathParameters,
                stageVariables, body, isBase64Encoded
            ''')

        self.event[key] = value
