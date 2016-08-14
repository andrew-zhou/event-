from functools import wraps
from datetime import datetime
from time import time
from traceback import extract_stack, format_list

_options = {
    'format': _default_format(),
    'time_function_calls': True,
    'log_stack_trace': True,
    'output_file': None
}

def set_options(**kwargs):
    for key, value in kwargs.items():
        _options[key] = value

def time_function_calls(should_time):
    _options['time_function_calls'] = should_time

def log_stack_trace(should_log):
    _options['log_stack_trace'] = should_log

def set_format(new_format):
    _options['format'] = new_format

def set_output_file(new_file):
    _options['output_file'] = new_file

def elog(event_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if _options['time_function_calls']:
                t1 = time()
            return_val = fn(*args, **kwargs)
            if _options['time_function_calls']:
                t2 = time()
            stack_trace = extract_stack(f=1)
            print(_output(event_name, _options['time_function_calls'] ? t2 - t1 : 0, stack_trace), file=_options['output_file'])
        return wrapper
    return decorator

def _output(event_name, duration, stack_trace, *args, **kwargs):
    output = '{0}\n\tTime: {1}\n\tCalled with arguments: {2}'
    if _options['time_function_calls']:
        output += '\n\tDuration: {3}'
    if _options['log_stack_trace']:
        output += '\n\tStacktrace: \n\t\t{4}'

    arg_string = ', '.join(map(lambda x : repr(x), args))
    if arg_string.length() > 0:
        arg_string += ', '.join(map(lambda key: repr(key) + ':' + repr(kwargs[key]), kwargs))
    stack_string = '\t\t'.join(format_list(stack_trace))

    return output.format(_options['format'].format(event_name), datetime.now().time(), arg_string, duration, stack_string)

def _default_format():
    return 'LOG: {0} triggered'
