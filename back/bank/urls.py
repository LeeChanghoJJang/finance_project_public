from django.urls import path
from . import views
from .views import UpdateDepositUserView

urlpatterns = [
    path('search/', views.deposit_search),  # 전체 예적금 검색
    path('search/<str:bank_name>/<str:intr_rate_type>/', views.deposit_search_by_params),  # 은행 및 이자율에 따른 검색
    path('save/',views.save), # 예적금 정보 저장(매일 API 저장 실행)
    path('main/',views.main), # 메인페이지 정보 반환
    path('clear/',views.clear), # 싹쓸어버리기 주의!!
    path('<int:deposit_id>/likes/', UpdateDepositUserView.as_view(), name='likes'), # 관심종목에 추가 예적금
    
] 