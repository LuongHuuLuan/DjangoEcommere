from rest_framework import serializers
from .models import Product

# class CustomPriceField(serializers.Field):
#     def to_representation(self, obj):
#         # Convert the integer to a string for representation
#         return str(obj)
#
#     def to_internal_value(self, data):
#         try:
#             # Convert the string to an integer
#             return int(data[0])
#         except ValueError:
#             raise serializers.ValidationError('Invalid price. Must be a number.')

class ProductSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=255)
    # introduce = serializers.Field
    # product_quantity = serializers.IntegerField(required=False, default=1)

    # image_url = serializers.SerializerMethodField('get_image_url')
    # video_url = serializers.SerializerMethodField('get_video_url')
    # price = CustomPriceField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'introduce', 'price', 'quantity', 'create_at', 'image', 'video')
        # fields = ('name', 'introduce', 'create_at', 'image', 'video')

    # def get_image_url(self, obj):
    #     return obj.image.url
    #
    # def get_video_url(self, obj):
    #     return obj.video.url
class ProductResponseSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=255)
    code = serializers.IntegerField()
    data = ProductSerializer(many=True)