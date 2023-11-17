from django.shortcuts import render, get_object_or_404
from .models import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .filters import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Avg
# Create your views here.

@api_view(['GET'])
def get_products(request):
    product = Product.objects.all()
    filter = ProductFilters(request.GET, queryset=product.order_by('id'))
    count = filter.qs.count()

    # Paginator
    res_per_page = 1
    paginator = PageNumberPagination()
    paginator.page_size = res_per_page
    queryset = paginator.paginate_queryset(filter.qs, request)

    serializers = ProductSerializers(queryset, many = True)
    return Response({
        "count":count,
        "res_per_page":res_per_page,
        "product": serializers.data,
        })

@api_view(['GET'])
def get_product(request, pk):
    product = get_object_or_404(Product, id = pk)
    serializers = ProductSerializers(product, many = False)
    return Response({"product": serializers.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = ProductSerializers(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data, user = request.user)
        res = ProductSerializers(product, many = False)
        return Response({"product":res.data})
    else:
        return Response(serializer.errors)

@api_view(['POST'])
@permission_classes({IsAuthenticated})
def update_product_image(request):
    data = request.data
    files = request.FILES.getlist('images')
    
    images = []
    for f in files:
        images = ProductImages.objects.create(product=Product(data['product']), images=f)
        images.append(images)
        serializers = ProductImagesSerializers(images, many = True)

    return Response(serializers.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({"error":"This is not your product to update"}, status=status.HTTP_401_UNAUTHORIZED)

    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']
    
    product.save()
    serializer = ProductSerializers(product, many = False)
    return Response({"product": serializer.data})

@api_view(['DELETE'])
@permission_classes({IsAuthenticated})
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response({"error":"This is not your product to Delete"})
    product.delete()
    return Response({'message':'product Delected succefully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_update_reviews(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    data = request.data
    review = product.reviews.filter(user = user)

    if data['ratings'] < 0 or data['ratings'] > 5:
        return Response({'error':'Rating has to be 1 to 5'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif review.exists():
        new_review = {
            "ratings":data['ratings'],
            "comment":data['comment']
            }
        review.update(**new_review)
        rating = product.reviews.aggregate(avg_rating = Avg('ratings'))

        product.ratings = rating['avg_rating']
        product.save()

        return Response({"message": "rating update succesfully"}, status=status.HTTP_201_CREATED)
    else:
        Review.objects.create(user=user, product=product, ratings=data['ratings'], comment=data['comment'])
        rating = product.reviews.aggregate(avg_rating=Avg('rating'))
        product.ratings = rating['avg_rating']
        product.save()
        return Response({'message':'Review created'}, status=status.HTTP_201_CREATED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_reviews(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)
    review = product.reviews.filter(user=user)

    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_rating=Avg('ratings'))
        if rating['avg_rating'] is None:
            rating['avg_rating'] = 0
        product.ratings = rating['avg_rating']
        product.save()
        return Response({'message': 'review deleted'}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'Review not found'}, status=status.HTTP_400_BAD_REQUEST)
    
