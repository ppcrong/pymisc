import datetime
import inspect


class printlib:

    @staticmethod
    def print(*args, **kwargs):
        stack = inspect.stack()

        # Get class name
        try:
            the_class = stack[1][0].f_locals["self"].__class__.__name__
        except KeyError as e:
            the_class = None

        # Get function name
        the_method = stack[1][0].f_code.co_name

        # Get line number
        the_line_number = stack[1][0].f_lineno

        # Get time
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]

        if the_class:
            print(
                "{} [{}.{}#{}] {}".format(timestamp, the_class, the_method, the_line_number, " ".join(map(str, args))),
                **kwargs)
        else:
            print("{} [{}#{}] {}".format(timestamp, the_method, the_line_number, " ".join(map(str, args))), **kwargs)

    @staticmethod
    def get_caller_info(level: int = 1):
        stack = inspect.stack()

        # Get class name
        try:
            the_class = stack[level][0].f_locals["self"].__class__.__name__
        except KeyError as e:
            the_class = None

        # Get function name
        the_method = stack[level][0].f_code.co_name

        # Get line number
        the_line_number = stack[level][0].f_lineno

        # Get time
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S.%f')[:-3]

        if the_class:
            return "{} [{}.{}#{}]".format(timestamp, the_class, the_method, the_line_number)
        else:
            return "{} [{}#{}]".format(timestamp, the_method, the_line_number)

    @staticmethod
    def draw_percent(percent, text, bar_len=20):
        import sys
        sys.stdout.write('\r')
        progress = ''
        for i in range(bar_len):
            if i < int(bar_len * percent):
                progress += '='
            else:
                progress += ' '
        sys.stdout.write(f'[ {progress} ] {percent * 100:.2f}%...{text}...')
        sys.stdout.flush()
