class NotebookTask:
    def __init__(self, path, parameters=None, timeout=86400, retry=0):
        self.path = path
        self.parameters = parameters
        self.timeout = timeout
        self.retry = retry
