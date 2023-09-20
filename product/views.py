from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

# Create your views here.

class ProductListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):

        # # get single product
        # if id:
        #     product = get_object_or_404(Product, id)
        #     serializer = ProductSerializer(product)
        #     return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        # checking for the parameters from the URL
        if request.query_params:
            products = Product.objects.filter(**request.query_params.dict()).order_by('-create_at')
        else:
            products = Product.objects.all().order_by('-create_at')
        if products:
            serializer = ProductSerializer(products, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

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

    def put(self, request, pk):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated]

        instance = get_object_or_404(Product, pk=pk)
        product = ProductSerializer(instance=instance, data=request.data)
        # check valid products
        if product.is_valid():
            product.save()
            return Response({"status": "success", "data": product.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated]

        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)

class ProductCRUD(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

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

    def put(self, request, pk):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated]

        instance = get_object_or_404(Product, pk=pk)
        product = ProductSerializer(instance=instance, data=request.data)
        # check valid products
        if product.is_valid():
            product.save()
            return Response({"status": "success", "data": product.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        authentication_classes = [TokenAuthentication, SessionAuthentication]
        permission_classes = [IsAuthenticated]

        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"status": "accepted"}, status=status.HTTP_202_ACCEPTED)