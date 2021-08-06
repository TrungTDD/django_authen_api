from rest_framework import serializers


class TaskSerializers(serializers.Serializer):
    title = serializers.CharField(max_length=256)
    description = serializers.CharField(max_length=256, required=False)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
