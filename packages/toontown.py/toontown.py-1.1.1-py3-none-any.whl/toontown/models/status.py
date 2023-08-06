__all__ = ['Status']

class Status:
    """Wrapper class for the /status response
    
    TODO: Get rest of response (potentially)
    
    Attributes
    ----------
    open : bool
        whether or not Toontown Rewritten is open
    """
    def __init__(self, **payload) -> None:
        self.open: bool = payload.get('open', False)
