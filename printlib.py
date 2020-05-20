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

        if the_class:
            print("[{}.{}#{}] {}".format(the_class, the_method, the_line_number, " ".join(map(str, args))), **kwargs)
        else:
            print("[{}#{}] {}".format(the_method, the_line_number, " ".join(map(str, args))), **kwargs)
