from rest_framework import serializers


class TTSRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
    language = serializers.CharField(default="en")
    voice = serializers.CharField(default="english_female")
