from pylambdatest.BaseLambdaTest import BaseLambdaTest

class AlexaLambdaTest(BaseLambdaTest):
    def __init__(self, context):
        event = {
            'header' : {
                'payloadVersion' : None,
                'namespace' : None,
                'name' : None
            },
            'payload' : {
                'switchControlAction' : None,
                'appliance' : {
                    'applianceId' : None,
                    'additionalApplianceDetails' : {}
                },
                "accessToken" : None
            }
        }
        super().__init__(context, event = event)

