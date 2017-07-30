from rest_framework import serializers
from demo.models import Book,Publisher, Author


class PublisherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    address = serializers.CharField(max_length=50)
    city = serializers.CharField(max_length=60)
    state_province = serializers.CharField(max_length=30)
    country = serializers.CharField(max_length=50)
    website = serializers.URLField()

    def create(self, validated_data):
        validated_data.pop("id")
        return Publisher.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.state_province = validated_data.get("state_province", instance.state_province)
        instance.country = validated_data.get("country", instance.country)
        instance.website = validated_data.get("website", instance.website)
        instance.save()
        return instance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "email")


