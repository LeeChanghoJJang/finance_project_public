from django.db import models
from stock.models import Stock
from django.conf import settings

# Create your models here.
class Review(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,related_name='reviews') # 해당 주식에 대한 리뷰 게시글 적기
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='write_reviews') # 각 유저별로 게시글 적기
    title = models.TextField() # 게시글 제목
    content = models.TextField() # 게시글 내용
    created_at = models.DateTimeField(auto_now_add=True) # 작성일자
    updated_at = models.DateTimeField(auto_now=True) # 수정일자

class Comment(models.Model):
    review = models.ForeignKey(Review,on_delete=models.CASCADE,related_name='comments') # 해당 게시글의 댓글
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='write_comments') # 유저가 작성한 댓글
    content = models.TextField() # 댓글 내용 


