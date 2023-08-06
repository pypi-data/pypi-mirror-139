import time

class BaseContext:
	def __init__(
		self,
		function_name = '', 
		function_version = '',
		invoked_function_arn = '',
		memory_limit_in_mb = '', 
		aws_request_id = '',
		log_group_name = '',
		log_stream_name = '',
		identity = {},
		client_context = {},
		function_execution_time = 900
	):
		self.function_name = function_name
		self.function_version = function_version
		self.invoked_function_arn = invoked_function_arn
		self.memory_limit_in_mb = memory_limit_in_mb
		self.aws_request_id = aws_request_id
		self.log_group_name = log_group_name
		self.log_stream_name = log_stream_name
		self.identity = identity
		self.client_context = client_context
		self._function_execution_time = function_execution_time

		#Protected variables for estimating how long a lambda
		#function takes to execute
		self._start_time = 0
		self._end_time = 0
		
	def start(self):
		self._start_time = time.time() * 1000

	def end(self):
		self._end_time = time.time() * 1000

	def get_remaining_time_in_millis(self):
		current_time = time.time() * 1000
		execution_timeout = self._start_time + self._function_execution_time * 1000
		return round(execution_timeout - current_time)

	def execution_time(self):
		return round(self._end_time - self._start_time)
