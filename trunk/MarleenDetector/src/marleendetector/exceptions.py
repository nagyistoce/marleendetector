class Error(Exception):
    """Base class for exceptions in the marleendetector."""
    pass

class FileNotFoundError(Error):
    """
    Exception raised when a file could not be found.
    Usually the file variable is None (NoneType)
    """
    
    def __init__(self, filename):
        """
            @param filename: the name of the file that could not be found
            @type filename: string, filelocation
        """
        self.filename = filename