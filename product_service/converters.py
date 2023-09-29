from django.urls import converters


class OrderNumberConverter:
    regex = '[0-9A-Fa-f]{32}'  # Matches 32 characters of 0-9, A-F, or a-f

    def to_python(self, value):
        return value

    def to_url(self, value):
        return str(value)
