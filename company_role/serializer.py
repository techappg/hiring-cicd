from rest_framework import serializers
from company_role.models import *

class InterviewwSerializer(serializers.ModelSerializer):
    class Meta:
        model=IntervieweeTestDetails
        fields ="__all__"