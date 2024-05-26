# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from bank.models import Deposit
from bank.serializers import DepositListSerializer
from rest_framework import status
from .serializers import UserSerializer, UserPKSerializer
from stock.serializers import UserStockSerializer
from stock.models import UserStock
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from stock.models import Stock
from stock.serializers import StockSerializer
from django.contrib.auth import get_user_model


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class GetUserStockView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        user_stocks = UserStock.objects.filter(user=user)
        user_serializer = UserSerializer(user)
        user_stock_serializer = UserStockSerializer(user_stocks, many=True)
        return Response({'user': user_serializer.data, 'user_stocks': user_stock_serializer.data})
    

class UpdateUserStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, stock_name):
        user = request.user
        stock = get_object_or_404(Stock, name=stock_name)

        # UserStock 객체가 존재하는지 확인
        user_stock = UserStock.objects.filter(user=user, stock=stock).first()

        if user_stock:
            # 이미 존재하는 경우 삭제
            user_stock.delete()
            action = 'removed'
        else:
            # 존재하지 않는 경우 새로 생성
            user_stock = UserStock(user=user, stock=stock, amount=1)
            user_stock.save()
            action = 'added'

        response_data = {
            'stock': StockSerializer(stock).data,  # 필요에 따라 적절한 Serializer 사용
            'action': action
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
@api_view(['GET','PUT','DELETE'])
def delete_userstock(request,stock_id):
    if request.method=='DELETE':
        userstock = UserStock.objects.get(stock = stock_id)
        userstock.delete()
        user_stocks = UserStock.objects.filter(user=request.user)
        user_serializer = UserSerializer(request.user)
        user_stock_serializer = UserStockSerializer(user_stocks, many=True)
        return Response({'user': user_serializer.data, 'user_stocks': user_stock_serializer.data})

class GetUserDepositView(APIView):
    def get(self, request):
        # 인증된 사용자에 대한 요청이므로, 현재 사용자를 기준으로 예금 정보를 가져옵니다.
        deposits = Deposit.objects.filter(users=request.user)
        # 여기서 필요한 형식으로 데이터를 가공하거나 직렬화합니다.
        data = DepositListSerializer(deposits,many=True)
        return Response({'user_deposits':data.data}) 
    
@api_view(['GET','PUT','DELETE'])
def delete_userdeposit(request,deposit_id):
    if request.method == 'DELETE':
        # 요청한 사용자와 연결된 Deposit을 찾습니다.
        user_deposit = Deposit.objects.filter(pk=deposit_id, users=request.user).first()
        if user_deposit:
            # 사용자와 Deposit 간의 관계를 제거합니다.
            user_deposit.users.remove(request.user)
            return Response({'message': 'User removed from Deposit'}, status=200)
        else:
            return Response({'message': 'Deposit not found or unauthorized'}, status=404)

@api_view(['GET'])
def get_all_users(request):
    if request.method == 'GET':
        users = get_user_model().objects.all()
        serializer = UserPKSerializer(users, many=True)
        # 'id:username' 형식의 JSON 생성
        users_dict = {user['id']: user['username'] for user in serializer.data}
        return Response(users_dict)
