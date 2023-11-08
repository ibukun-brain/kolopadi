from django.db import IntegrityError
from rest_framework import serializers

from loans.models import Borrower, BorrowerAsset, Lender, LenderProposal, LoanListing


class LenderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Lender
        fields = [
            "user",
            "username",
            "bio",
            "verified",
            "address",
        ]
        extra_kwargs = {
            "verified": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        request = self.context["request"]
        lender = Lender()
        try:
            lender = Lender.objects.create(**validated_data)
        except IntegrityError:
            lender = Lender.objects.get(user=request.user)
        return lender


class BorrowerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Borrower
        fields = [
            "user",
            "username",
            "bio",
            "verified",
            "address",
        ]

        extra_kwargs = {
            "verified": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        request = self.context["request"]
        borrower = Borrower()
        try:
            borrower = Borrower.objects.create(**validated_data)
        except IntegrityError:
            borrower = Borrower.objects.get(user=request.user)
        return borrower


class LoanListingSerializer(serializers.ModelSerializer):
    borrower = serializers.CharField(source="borrower.username", read_only=True)

    class Meta:
        model = LoanListing
        fields = [
            "uid",
            "title",
            "borrower",
            "loan_amount",
            "interest_rate",
            "loan_tenure_in_months",
            "reason_for_loan",
            "ability_to_repay",
        ]
        extra_kwargs = {
            "uid": {
                "read_only": True,
            }
        }


class BorrowerAssetSerializer(serializers.ModelSerializer):
    loan_listing = serializers.StringRelatedField()

    class Meta:
        model = BorrowerAsset
        fields = [
            "uid",
            "loan_listing",
            "asset_type",
            "asset_value",
            "ownership_percentage",
            "possession_since",
        ]
        extra_kwargs = {
            "uid": {
                "read_only": True,
            }
        }


class LoanProposalCreateSerializer(serializers.ModelSerializer):
    loan_listing = serializers.StringRelatedField()
    lender = LenderSerializer(many=False, read_only=True)

    class Meta:
        model = LenderProposal
        fields = [
            "uid",
            "lender",
            "loan_listing",
            "cancel_date",
            "created_at",
        ]
        extra_kwargs = {
            "uid": {
                "read_only": True,
            },
            "cancel_date": {
                "read_only": True,
            },
        }


class LoanProposalUpdateSerializer(serializers.ModelSerializer):
    loan_listing = serializers.StringRelatedField()
    lender = LenderSerializer(many=False, read_only=True)

    class Meta:
        model = LenderProposal
        fields = [
            "uid",
            "lender",
            "cancel_date",
            "loan_listing",
            "created_at",
        ]
        extra_kwargs = {
            "uid": {
                "read_only": True,
            }
        }
