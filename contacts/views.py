from rest_framework import viewsets
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing contact instances.
    """
    serializer_class = ContactSerializer

    def get_queryset(self):
        # Always return the latest queryset in descending order (newest first)
        return Contact.objects.all().order_by('-id')

    def perform_create(self, serializer):
        instance = serializer.save()
        # Optional: Print to console for debug purposes
        print(f"New contact saved: {instance.name} - {instance.email}")
