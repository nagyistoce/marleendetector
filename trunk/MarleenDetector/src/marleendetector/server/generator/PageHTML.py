class PageHTML:
    
    def __init__(self):
        pass
    
    def getHeader(self):
        """
            Returns the header of a HTML page
            returns a list of strings
        """
        lines = []
        lines.append("<html>")
        return lines
    
    def getFooter(self):
        """
            Returns the footer of a HTML page
            returns a list of strings
        """
        lines = []
        lines.append("</html>")
        return lines