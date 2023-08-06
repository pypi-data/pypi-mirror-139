import os
import warnings

class BaseLambdaTest:
    def __init__(self, context, event = {}):
        self.context = context
        self.event = event
        self.environment = {}

    def test(self, func):

        #Set environment variables for Lambda function execution
        for key in self.environment.keys():
            os.environ[key] = self.environment[key]

        self.context.start()
        response = func(self.event, self.context)
        self.context.end()
        return response

    def set_environment_var(self, key, value):
        self.environment[str(key)] = str(value)