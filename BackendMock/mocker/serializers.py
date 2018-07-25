from rest_framework import serializers
from .models import MockItem, MockSlot, MockCondition

__author__ = 'sun_yang'


class MockConditionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MockCondition
        fields = ('key', 'value', 'compFunc', 'mockSlot', 'id')


class MockSlotSerializer(serializers.ModelSerializer):

    # conditions = serializers.HyperlinkedRelatedField(many=True, view_name='condition-detail', read_only=True)
    # conditions = PrimaryKeyRelatedField(many=True, read_only=True)
    conditions = MockConditionSerializer(many=True, read_only=True)

    class Meta:
        model = MockSlot
        fields = ('value', 'desc', 'compMethod', 'active', 'mockItem', 'conditions', 'id')


class MockItemSerializer(serializers.ModelSerializer):

    # slots = PrimaryKeyRelatedField(many=True, read_only=True)
    # slots = serializers.HyperlinkedRelatedField(many=True, view_name='slot-detail', read_only=True)
    slots = MockSlotSerializer(many=True, read_only=True)

    class Meta:
        model = MockItem
        fields = ('activeType', 'redirect', 'finalTarget', 'desc', 'url', 'slots', 'id')

