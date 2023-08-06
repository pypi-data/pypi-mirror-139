from pylambdatest.BaseLambdaTest import BaseLambdaTest

class CloudFormationLambdaTest(BaseLambdaTest):
    def __init__(self, context):
        event = {
            'RequestType' : None,
            'ServiceToken' : None,
            'ResponseURL' : None,
            'StackId' : None,
            'RequestId' : None,
            'LogicalResourceId' : None,
            'ResourceType' : None,
            'ResourceProperties' : {}
        }
        super().__init__(self, context, event = event)

    def add_event_value(self, key, value):
        if key not in list(self.event.keys()):
            raise Exception('''
                Invalid event value: Cloud Formation Event only supports the following event values:
                RequestType, ServiceToken, ResponseURL, StackId, RequestId, LogicalResourceId,
                ResourceType, ResourceProperties
            ''')
        self.event[key] = value

