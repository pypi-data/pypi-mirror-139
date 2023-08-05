class ValidityError(Exception):
    """Bot Status Error"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
