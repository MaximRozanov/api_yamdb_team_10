from rest_framework import serializers
from django.db.models import Avg, IntegerField


class RatingByScoresField(serializers.RelatedField):
    def to_representation(self, data):
        return data.aggregate(Avg('score', output_field=IntegerField()))[
            'score__avg'
        ]
