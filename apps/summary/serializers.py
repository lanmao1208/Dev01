import re

from rest_framework import serializers
from rest_framework import validators

from reports.models import Reports
from utils.common import datetime_fmt


class SummaryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        exclude = ('update_time',)

        extra_kwargs = {
            'html': {
                'write_only': True
            }
        }


