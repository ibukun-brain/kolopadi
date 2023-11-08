from rest_framework import generics, permissions
from rest_framework.response import Response

from rest_framework.serializers import ValidationError

from loans.api.custom_permissions import IsLenderOrReadOnly, IsLoanBorrowerOrReadOnly
from loans.api.serializers import (
    BorrowerAssetSerializer,
    BorrowerSerializer,
    LenderSerializer,
    LoanListingSerializer,
    LoanProposalCreateSerializer,
)
from loans.models import Borrower, BorrowerAsset, Lender, LenderProposal, LoanListing


class LenderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LenderSerializer

    def get_queryset(self):
        qs = Lender.objects.select_related("user").all()
        return qs

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class LenderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsLenderOrReadOnly,
    ]
    serializer_class = LenderSerializer
    queryset = Lender.objects.all()

    def get(self, request, *args, **kwargs):
        """
        The endpoint checks the current user that's logged in whether user is a lender
        """
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        qs = self.request.user.lender
        try:
            qs = self.request.user.lender
        except Lender.DoesNotExist:
            return Response(
                {"error": "This user is not a lender"}, status=400
            )
        if not qs.verified:
            raise ValidationError(
                {"detail": "Your account is under verification"}, code=200
            )
        return qs

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class BorrowerListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BorrowerSerializer

    def get_queryset(self):
        qs = Borrower.objects.select_related("user").all()
        return qs

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class BorrowerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsLenderOrReadOnly,
    ]
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()

    def get(self, request, *args, **kwargs):
        """
        The endpoint checks the current user that's logged in whether user is a borrower
        """
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        qs = self.request.user.borrower
        try:
            qs = self.request.user.borrower
        except Borrower.DoesNotExist:
            return Response(
                {"error": "This user is not a lender"},
                status=400
            )
        if not qs.verified:
            raise ValidationError(
                {"detail": "Your account is under verification"}, code=200
            )
        return qs

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class BorrowerAssetListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BorrowerAssetSerializer
    lookup_field = "loan_listing__uid"

    def get_queryset(self):
        loan_listing_uid = self.kwargs["loan_listing_uid"]
        qs = BorrowerAsset.objects.select_related("loan_listing").filter(
            loan_listing__uid=loan_listing_uid
        )
        return qs

    def perform_create(self, serializer):
        loan_listing_uid = self.kwargs["loan_listing_uid"]
        loan_listing = LoanListing.objects.get(uid=loan_listing_uid)
        return serializer.save(loan_listing=loan_listing)

    def post(self, request, *args, **kwargs):
        """
        Endpoint for lenders to create a borrower asset for a loan
        """
        return self.create(request, *args, **kwargs)


class LoanListingListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanListingSerializer
    # filter_backends = []
    filterset_fields = ["loan_amount", "interest_rate", "loan_tenure_in_months"]

    def get_queryset(self):
        qs = (
            LoanListing.objects.select_related("borrower")
            .order_by(
                "-loan_amount",
                "-created_at",
                "-updated_at",
            )
            .filter(borrower=self.request.user.borrower)
        )
        return qs

    def get(self, request, *args, **kwargs):
        """
        API endpoint for all loans
        """
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(borrower=self.request.user.borrower)


class LoanListingRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsLoanBorrowerOrReadOnly]
    serializer_class = LoanListingSerializer
    queryset = LoanListing.objects.all()
    lookup_field = "uid"


class LoanProposalListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanProposalCreateSerializer
    lookup_field = "loan_listing__uid"

    def get_queryset(self):
        qs = LenderProposal.objects.select_related("lender", "loan_listing").filter(
            lender=self.request.user.lender
        )
        return qs

    def perform_create(self, serializer):
        loan_listing_uid = self.kwargs["loan_listing_uid"]
        loan_listing = LoanListing.objects.get(uid=loan_listing_uid)
        return serializer.save(
            lender=self.request.user.lender, loan_listing=loan_listing
        )

    def post(self, request, *args, **kwargs):
        """
        Endpoint for lenders to create a proposal for a loan
        """
        return self.create(request, *args, **kwargs)
