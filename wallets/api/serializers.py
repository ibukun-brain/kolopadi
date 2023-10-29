from rest_framework import serializers

from wallets.models import Bank, Transaction, Wallet


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ("name", "bank_code")


class UserWalletSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Wallet
        fields = [
            "user",
            "account_name",
            "account_number",
            "account_reference",
            "barter_id",
            "balance",
            "bank",
            "is_hidden",
        ]
        extra_kwargs = {
            "account_reference": {
                "read_only": True,
            },
            "account_name": {
                "read_only": True,
            },
            "account_number": {
                "read_only": True,
            },
            "barter_id": {
                "read_only": True,
            },
            "balance": {
                "read_only": True,
            },
            "bank": {
                "read_only": True,
            },
        }

    def update(self, instance, validated_data):
        instance.is_hidden = validated_data.get("is_hidden", instance.is_hidden)
        instance.save()
        return instance


class WalletTransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = [
            "uid",
            "wallet",
            "type",
            "amount",
            "remarks",
            "reference",
            "date",
            "transfer_status",
            "external_recipient",
            "external_recipient_account_no",
            "external_recipient_bank",
            "transfer_status",
        ]
