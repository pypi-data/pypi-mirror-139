def group():
    functions = []
    def handler(func):functions.append(func)
    handler.functions = functions
    return handler