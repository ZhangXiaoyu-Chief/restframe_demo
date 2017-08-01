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
    full_address = serializers.CharField(source="get_full_address", read_only=True)

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


class HelloField(serializers.Field):

    def to_representation(self, obj):
        # 重写to_representation方法实现序列化
        return "%s %s" % ("hello", obj)


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    hello = HelloField(read_only=True, source="first_name")

    class Meta:
        model = Author
        fields = ("id", "first_name", "last_name", "email", "name", "hello")

    def get_name(self, obj):
        # name字段的实现方法，它接收一个参数obj，即要序列化的对象
        return "%s %s" % (obj.first_name, obj.last_name)


class AuthorListField(serializers.RelatedField):
    """自定义作者关联字段"""
    def to_representation(self, obj):
        return AuthorSerializer(obj).data


class BookSerializer(serializers.ModelSerializer):

    publisher = serializers.StringRelatedField()
    publisher_url = serializers.HyperlinkedRelatedField(read_only=True, source="publisher", view_name="publisher_detail")
    publisher_name = serializers.SlugRelatedField(read_only=True, slug_field="name", source="publisher")
    author_list = AuthorListField(source="authors", many=True, read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "authors", "publisher", "publication_date", "publisher_url", "publisher_name", "author_list")

