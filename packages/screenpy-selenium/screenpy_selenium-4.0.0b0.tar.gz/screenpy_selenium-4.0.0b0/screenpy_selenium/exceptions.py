from screenpy.exceptions import AbilityError, ScreenPyError


class TargetingError(ScreenPyError):
    """There is an issue preventing Target acquisition."""


class BrowsingError(AbilityError):
    """BrowseTheWeb encountered an error."""
