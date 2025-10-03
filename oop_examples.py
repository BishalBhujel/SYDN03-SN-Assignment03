# Demonstrates required OOP concepts

# Encapsulation + Method Overriding
class BaseModel:
    def __init__(self, name):
        self._name = name  # encapsulated attribute

    def info(self):
        return f"Model: {self._name}"

class ExtendedModel(BaseModel):
    def info(self):  # overriding
        return f"Extended Model: {self._name}"

# Polymorphism
def describe(model: BaseModel):
    return model.info()

# Multiple Inheritance
class LoggingMixin:
    def log(self, message):
        print(f"[LOG]: {message}")

class MultiModel(ExtendedModel, LoggingMixin):
    def run(self):
        self.log(f"Running {self._name}")

# Decorators
def model_decorator(func):
    def wrapper(*args, **kwargs):
        print("Decorator: Starting model execution...")
        result = func(*args, **kwargs)
        print("Decorator: Model execution finished.")
        return result
    return wrapper

class DecoratedModel:
    @model_decorator
    def run(self):
        return "Model run completed!"
