from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ProductSerializer, ProductResponseSerializer
from .models import Product
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiExample


# Create your views here.

class ProductListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_permissions(self):
        method = self.request.method
        if method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    @extend_schema(
        request=None,
        responses={200: ProductResponseSerializer},
        examples=[
            OpenApiExample(
                'Example',
                value={
                    "status": "success",
                    "code": 200,
                    "data": [
                        {
                            "id": 1,
                            "name": "Product 1",
                            "introduce": "This is product 1",
                            "price": 34990000,
                            "quantity": 10,
                            "create_at": "2023-09-20T10:43:48.898317+07:00",
                            "image": "/media/images_dir/product1.jpg",
                            "video": "/media/videos_dir/product1.jpg"
                        },
                    ]
                },
                response_only=True,
            )
        ],
    )
    def get(self, request):
        # checking for the parameters from the URL
        if request.query_params:
            products = Product.objects.filter(**request.query_params.dict()).order_by('-create_at')
        else:
            products = Product.objects.all().order_by('-create_at')
        if products:
            serializer = ProductSerializer(products, many=True)
            return Response({"status": "success", "code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):

        product = ProductSerializer(data=request.data)
        # validating for already existing data
        if Product.objects.filter(name=request.data["name"]).exists():
            raise serializers.ValidationError('This data already exists')
        # check valid products
        if product.is_valid():
            product.save()
            return Response({"status": "success", "data": product.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    serializer_class = ProductSerializer

    def post(self, request):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]

        product = ProductSerializer(data=request.data)
        # validating for already existing data
        if Product.objects.filter(name=request.data["name"]).exists():
            raise serializers.ValidationError('This data already exists')
        # check valid products
        if product.is_valid():
            product.save()
            return Response({"status": "success", "data": product.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UpdateProductView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    # def get_permissions(self):
    #     method = self.request.method
    #     if method == 'GET':
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]

    def put(self, request, pk):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]

        instance = get_object_or_404(Product, pk=pk)
        product = ProductSerializer(instance=instance, data=request.data)
        # check valid products
        if product.is_valid():
            product.save()
            return Response({"status": "success", "data": product.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # @permission_classes([IsAuthenticated])
    def delete(self, request, pk):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]

        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)
