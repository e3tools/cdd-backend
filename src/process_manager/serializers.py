from rest_framework import serializers
from process_manager.models import FormField

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = "__all__"