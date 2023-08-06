from pylambdatest.BaseLambdaTest import BaseLambdaTest

class CodePipelineLambdaTest(BaseLambdaTest):
	def __init__(self, context):
		event = {
			'CodePipeline.job' : {
				'id' : None,
				'accountId' : None,
				'data' : {
					'actionConfiguration' : {
						'configuration' : {
							'FunctionName' : None,
							'UserParameters' : None
						}
					},
					'inputArtifacts' : [],
					'outputArtifacts' : [],
					'artifactCredentials' : {}
				}
			}
		}
		super().__init__(self, context, event = event)

	def add_event_value(self, key, value):
		if key not in list(self.event['CodePipeline.job'].keys()):
			raise Exception('''
				pass
			''')