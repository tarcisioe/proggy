"""Error classes for Proggy."""


class ProggyError(Exception):
    """Base class for all Proggy errors."""


class ProgressValueError(ProggyError):
    """Represent a value error during the manipulation of a progress bar.

    E.g.: Progress being set higher than total.
    """
