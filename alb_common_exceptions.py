class ALBCommonExceptions(Exception):
    """Base class for exceptions in this module."""
    pass

class NoEc2InstanceFoundException(ALBCommonExceptions):
    """Exception raised for no instances being found.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg


    def __str__(self):
        return repr(self.msg)
class FailedToReachStateException(ALBCommonExceptions):
    """Exception raised for an instance never reaching the desired state.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg


    def __str__(self):
        return repr(self.msg)
