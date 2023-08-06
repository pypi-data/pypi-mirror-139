# PyLambdaTest

PyLambdaTest is a simple Python library for testing AWS Lambda functions locally.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyLambdaTest.

```bash
pip install pylambdatest
```

## Usage

```python
from pylambdatest import create_test
import time

#Example function to test
def post_route(event, context):
    time.sleep(2)
    return {
        'statusCode' : 200,
        'body' : 'This is a success'
    }

#Create API Gateway Test
api_gateway_test = create_test('apigateway')

#Perform test
response = api_gateway_test.test(post_route)

#See how long function took to execute in milliseconds
print(api_gateway_test.context.execution_time())

```

## License
[GNU GPL-V3](https://www.gnu.org/licenses/gpl-3.0.html)