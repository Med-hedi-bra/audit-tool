from rest_framework import serializers
from .models import ZapScan 

class ZapScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZapScan
        fields = ["id","target","file_name", "created_at", "progress"]   