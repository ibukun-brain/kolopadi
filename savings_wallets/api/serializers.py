from rest_framework import serializers

from savings_wallets.models import Savings, SavingsCategory


class SavingsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsCategory
        fields = ("name", "slug")


class SavingsSerializer(serializers.ModelSerializer):
    goal_title = serializers.CharField(source="name")
    category = SavingsCategorySerializer(many=False, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Savings
        fields = [
            "uid",
            "user",
            "goal_title",
            "category",
            "frequency",
            "frequency_amount",
            "amount_to_save",
            "amount_saved",
            "start_date",
            "next_savings_date",
            "end_date",
            "is_liquidated",
            "status",
            "type_of_savings",
        ]
        extra_kwargs = {
            "status": {
                "read_only": True,
            },
            "is_liquidated": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        return Savings.objects.create(**validated_data)
