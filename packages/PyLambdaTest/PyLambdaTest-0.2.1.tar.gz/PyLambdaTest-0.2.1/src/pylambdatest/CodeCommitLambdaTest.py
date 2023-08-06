from pylambdatest.BaseLambdaTest import BaseLambdaTest

class CodeCommitLambdaTest(BaseLambdaTest):
    def __init__(self, context):
        event = {
            'Records' : []
        }
        super().__init__(context, event = event)

    def add_event_record(
        self,
        aws_region = 'us-east-1',
        code_commit = {},
        event_id = None,
        event_name = None,
        event_part_number = 0,
        event_source_arn = None,
        event_time = None,
        event_total_parts = 0,
        event_trigger_config_id = None,
        event_trigger_name = None,
        event_version = '1.0',
        user_identity_arn = None
    ):
        self.event['Records'].append({
            'awsRegion' : aws_region,
            'codecommit' : code_commit,
            'eventId' : event_id,
            'eventName' : event_name,
            'eventPartNumber' : event_part_number,
            'eventSource' : 'aws:codecommit',
            'eventSourceARN' : event_source_arn,
            'eventTime' : event_time,
            'eventTotalParts' : event_total_parts,
            'eventTriggerConfigId' : event_trigger_config_id,
            'eventTriggerName' : event_trigger_name,
            'eventVersion' : event_version,
            'userIdentityARN' : user_identity_arn
        })