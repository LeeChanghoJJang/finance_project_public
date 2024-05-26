from django.urls import path
from . import views

urlpatterns = [
    path('<str:stock_name>/search/',views.stock_search), # 주식 기본 페이지 조회
    path('<str:stock_name>/search_detail/',views.stock_search_detail), # 주식 상세 페이지 조회
    path('save/',views.save), # 주식 정보 저장 
    path('clear/',views.clear), # 모든 정보 지우기
    path('recommend/<int:standard>/',views.recommend), # 상품 추천 알고리즘
    path('<str:stock_name>/article/', views.article_list), # 게시글 GET,POST
    path('<str:stock_name>/article/<int:article_pk>/', views.article_detail), # 게시글 GET,PUT,DELETE
    path('<str:stock_name>/article/<int:article_pk>/comments/', views.comment_list), # 댓글 GET,POST
    path('<str:stock_name>/article/<int:article_pk>/comments/<int:comment_pk>/', views.comment_delete) # 댓글 DELETE
]
