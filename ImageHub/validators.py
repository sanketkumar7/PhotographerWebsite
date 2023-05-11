from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.exceptions import ValidationError

class MaxFileSizeValidator(MaxValueValidator):
    def __call__(self, value):
        if hasattr(value, 'size'):
            size = value.size
        else:
            size = len(value)
        if size > self.limit_value:
            raise ValidationError(self.message, code=self.code)
class MinFileSizeValidator(MinValueValidator):
    def __call__(self, value):
        if hasattr(value, 'size'):
            size = value.size
        else:
            size = len(value)
        if size < self.limit_value:
            raise ValidationError(self.message, code=self.code)
