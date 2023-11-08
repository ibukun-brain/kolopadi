from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from home.api import custom_permissions
from savings_wallets.api.serializers import (
    SavingsCategorySerializer,
    SavingsSerializer,
    SavingsWithdrawalSerializer,
)
from savings_wallets.models import Savings, SavingsCategory


class SavingsCategoryAPIView(generics.ListAPIView):
    serializer_class = SavingsCategorySerializer
    queryset = SavingsCategory.objects.all()


class SavingsListAPIView(generics.ListCreateAPIView):
    serializer_class = SavingsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsSavingsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        qs = Savings.objects.select_related("category", "user").filter(
            user=self.request.user, is_liquidated=False
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


class SavingsDetailAPIView(generics.RetrieveAPIView):
    serializer_class = SavingsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsSavingsOwnerOrReadOnly,
    ]
    lookup_field = "uid"

    def get_queryset(self):
        qs = Savings.objects.select_related("category", "user").filter(
            user=self.request.user,
            is_liquidated=False,
            status="started",
        )
        return qs

    def get(self, request, *args, **kwargs):
        """
        Returns a single savings/goal
        """
        return self.retrieve(request, args, kwargs)


class SavingsWithdrawalAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        custom_permissions.IsSavingsOwnerOrReadOnly,
    ]
    lookup_field = "uid"
    serializer_class = SavingsWithdrawalSerializer
    allowed_methods = ["post"]

    def get_queryset(self):
        qs = Savings.objects.select_related("category", "user").filter(
            user=self.request.user, is_liquidated=False, status="started"
        )
        return qs

    def post(self, request, *args, **kwargs):
        """
        Endpoint to withdraw a Savings/Goals
        """
        print(request.GET)
        serializer = SavingsWithdrawalSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
