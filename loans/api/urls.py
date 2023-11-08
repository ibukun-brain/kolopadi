from django.urls import path

from loans.api.views import (
    BorrowerAssetListCreateAPIView,
    BorrowerListCreateAPIView,
    BorrowerRetrieveUpdateAPIView,
    LenderListCreateAPIView,
    LenderRetrieveUpdateAPIView,
    LoanListingListCreateAPIView,
    LoanListingRetrieveUpdateDeleteAPIView,
    LoanProposalListCreateAPIView,
)

app_name = "loans"

urlpatterns = [
    path(
        "loans/listings/", LoanListingListCreateAPIView.as_view(), name="loan-listing"
    ),
    path(
        "loans/listings/<uuid:uid>/",
        LoanListingRetrieveUpdateDeleteAPIView.as_view(),
        name="loan-listing-detail",
    ),
    path(
        "loans/listings/<uuid:loan_listing_uid>/assets/",
        BorrowerAssetListCreateAPIView.as_view(),
        name="loan-listing-assets",
    ),
    path(
        "loans/listings/<uuid:loan_listing_uid>/proposals/",
        LoanProposalListCreateAPIView.as_view(),
        name="loan-listing-proposals",
    ),
    path("loans/lenders/", LenderListCreateAPIView.as_view(), name="lenders"),
    path("loans/lender/", LenderRetrieveUpdateAPIView.as_view(), name="lenders"),
    path("loans/borrowers/", BorrowerListCreateAPIView.as_view(), name="borrowers"),
    path("loans/borrower/", BorrowerRetrieveUpdateAPIView.as_view(), name="borrower"),
]
