from rest_framework import serializers

from .models import RedirectRule


class RedirectRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedirectRule
        fields = "__all__"
        read_only_fields = ["id", "redirect_identifier", "owner", "created", "modified"]

    def validate(self, data):
        if "redirect_url" in data and not data["redirect_url"].startswith("http"):
            raise serializers.ValidationError(
                "The redirect URL must start with 'http' or 'https'."
            )
        return data
