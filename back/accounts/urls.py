# urls.py
from django.urls import path
from .views import UserUpdateView,GetUserStockView,GetUserDepositView
from . import views
urlpatterns = [
    path('', UserUpdateView.as_view(), name='mypage'),
    path('get_user_stocks/', GetUserStockView.as_view(), name='get_user_stocks'),
    path('get_user_deposits/', GetUserDepositView.as_view(), name='get_user_deposits'),
    path('create_userstock/<str:stock_name>/',views.UpdateUserStockView.as_view(),name='update_user_stock'), # 스톡 생성하기
    path('delete_userstock/<int:stock_id>/',views.delete_userstock), # 삭제하기 
    path('delete_userdeposit/<int:deposit_id>/',views.delete_userdeposit), # 삭제하기
    path('get_all_users/', views.get_all_users) 
]