from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import requests
from django.conf import settings
from django.db.models import Max
import xml.etree.ElementTree as ET
import xml.dom.minidom
import json
import urllib.request
from .serializers import CommentSerializer,ReviewSerializer
from .models import Review,Comment
from stock.models import Stock
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

# 무조건 해야할 것은 user를 임시로 입력하는 것이 아닌 받아왔을 때 한번더 테스트 필요   

# 게시글 생성 함수(게시글을 생성하여 DB에 저장하고, 게시글 정보를 반환한다.)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_article(request,stock_pk):
    stock = get_object_or_404(Stock,pk=stock_pk)
    data = request.data.copy()
    data['stock'] = stock.pk
    # data['user'] = request.user.pk
    
    if request.method =='POST':
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
    
# 게시글 조회, 수정, 삭제 함수(게시글을 조회, 수정, 삭제하여 DB에 저장하고, 게시글 정보를 반환한다.)
@api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticated])
def article(request,stock_pk,article_pk):
    stock = get_object_or_404(Stock,pk=stock_pk)
    review = get_object_or_404(Review,pk=article_pk, stock=stock)
    if request.method=='GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    elif request.method=='PUT':
        serializer = ReviewSerializer(review,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method=='DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# 댓글 생성 함수(댓글을 생성하여 DB에 저장하고, 댓글 정보를 반환한다.)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_comments(request, article_pk):
    review = get_object_or_404(Review, pk=article_pk)
    serializer = CommentSerializer(data=request.data, context={'review': review})
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 조회, 수정, 삭제 함수(댓글을 조회, 수정, 삭제하여 DB에 저장하고, 댓글 정보를 반환한다.)
@api_view(['GET','PUT','DELETE'])
# @permission_classes([IsAuthenticated])
def comments(request,article_pk,comments_pk):
    comment = get_object_or_404(Comment,pk=comments_pk,review__pk=article_pk)
    if request.method=='GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer = CommentSerializer(comment,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method=='DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


