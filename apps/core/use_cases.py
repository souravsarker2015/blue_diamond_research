class BaseUseCase:
    def is_valid(self):
        return True

    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")

    def _factory(self):
        raise NotImplementedError("Subclasses should implement this!")
