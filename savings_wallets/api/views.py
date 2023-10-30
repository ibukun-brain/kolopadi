from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from home.api import custom_permissions
from savings_wallets.api.serializers import SavingsCategorySerializer, SavingsSerializer
from savings_wallets.models import Savings, SavingsCategory


class SavingsCategoryAPIView(generics.ListAPIView):
    serializer_class = SavingsCategorySerializer
    queryset = SavingsCategory.objects.all()

    def list(self, request, *args, **kwargs):
        """
        This endpoint returns Savings Category
        """
        return super().list(request, *args, **kwargs)


class SavingsAPIView(generics.ListCreateAPIView):
    serializer_class = SavingsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsSavingsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        qs = Savings.objects.select_related("category", "user").filter(
            user=self.request.user
        )
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        request=SavingsSerializer,
        responses=SavingsSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        This endpoint returns Savings/Goals of a user
        """
        return self.create(request, *args, **kwargs)
