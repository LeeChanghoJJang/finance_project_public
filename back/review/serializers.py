from rest_framework import serializers
from .models import Review,Comment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['review',]
        
    def create(self, validated_data):
        review = self.context['review']
        return Comment.objects.create(review=review, **validated_data)