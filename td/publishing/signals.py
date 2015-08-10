from django.dispatch import Signal

published = Signal(providing_args=["obs"])
