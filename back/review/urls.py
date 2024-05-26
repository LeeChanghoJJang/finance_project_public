from django.urls import path
from . import views

urlpatterns = [
    path('create_article/<int:stock_pk>/',views.create_article), # 게시글 생성
    path('article/<int:stock_pk>/<int:article_pk>/',views.article), # 게시글 조회 / 수정 / 삭제
    path('create_comments/<int:article_pk>/',views.create_comments), # 댓글 생성 
    path('comments/<int:article_pk>/<int:comments_pk>/',views.comments), # 댓글 조회 / 수정 / 삭제 / 생성 
]
