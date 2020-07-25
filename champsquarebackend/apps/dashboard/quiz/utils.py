class QuizCreateSessionData(object):
    """
    Responsible for marshalling all the quiz create session data

    Multi-stage quiz create often require several forms to be submitted and their
    data persisted until the final step is competed. This class helps store and
    organise quiz create form data until it is required to write out the final
    step.
    """
    SESSION_KEY = 'quiz_create_data'

    def __init__(self, request):
        self.request = request
        if self.SESSION_KEY not in self.request.session:
            self.request.session[self.SESSION_KEY] = {}

    def _check_namespace(self, namespace):
        """
        Ensure a namespace within the session dict is initialised
        """
        if namespace not in self.request.session[self.SESSION_KEY]:
            self.request.session[self.SESSION_KEY][namespace] = {}

    def _get(self, namespace, key, default=None):
        """
        Return a value from within a namespace
        """
        self._check_namespace(namespace)
        if key in self.request.session[self.SESSION_KEY][namespace]:
            return self.request.session[self.SESSION_KEY][namespace][key]
        return default

    def _set(self, namespace, key, value):
        """
        Set a namespaced value
        """
        self._check_namespace(namespace)
        self.request.session[self.SESSION_KEY][namespace][key] = value
        self.request.session.modified = True

    def _unset(self, namespace, key):
        """
        Remove a namespaced value
        """
        self._check_namespace(namespace)
        if key in self.request.session[self.SESSION_KEY][namespace]:
            del self.request.session[self.SESSION_KEY][namespace][key]
            self.request.session.modified = True

    def _flush_namespace(self, namespace):
        """
        Flush a namespace
        """
        self.request.session[self.SESSION_KEY][namespace] = {}
        self.request.session.modified = True

    def flush(self):
        """
        Flush all session data
        """
        self.request.session[self.SESSION_KEY] = {}

    