from elog import set_options, time_function_calls, log_stack_trace, set_format, set_output_file, elog
from unittest import TestCase
from unittest.mock import patch

# TODO: Implement tests
class ElogTest(TestCase):
    @elog('test')
    def foo(self):
        pass
