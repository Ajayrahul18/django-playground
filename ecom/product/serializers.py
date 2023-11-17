from rest_framework import serializers 
from .models import *



class ReviewSerializers(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"

class ProductImagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = "__all__"

class ProductSerializers(serializers.ModelSerializer):
    
    images = ProductImagesSerializers(many=True, read_only = True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only=True)
    class Meta:
        model = Product
        fields = ("id","name", "description", "price", "brand", "category", "stock","ratings", "user", "reviews", "images")
        extra_kwargs = {
            "name":{'required': True},
            "description":{'required': True},
            "price":{'required': True},
            "brand":{'required': True},
            "ratings":{'required': True},
            }
        
        #obj - Current product data
    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        serializer = ReviewSerializers(reviews, many=True)
        return serializer.data


