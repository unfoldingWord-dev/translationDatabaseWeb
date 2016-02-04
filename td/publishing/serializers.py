from td.publishing.models import PublishRequest
from rest_framework import serializers


# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
# that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization,
# allowing parsed data to be converted back into complex types, after first validating the incoming data.
# http://www.django-rest-framework.org/api-guide/serializers/
class PublishRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishRequest
        fields = ('id', 'requestor', 'resource_type', 'language', 'checking_level', 'source_text', 'source_version',
                  'contributors', 'requestor_email', 'license_title', 'created_at')
        read_only_fields = ('id', 'created_at',)


class ApprovedRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishRequest
        fields = ('id', 'requestor', 'resource_type', 'language', 'checking_level', 'source_text', 'source_version',
                  'contributors', 'requestor_email', 'license_title', 'created_at', 'approved_at')
        read_only_fields = ('id', 'requestor', 'resource_type', 'language', 'checking_level', 'source_text', 'source_version',
                            'contributors', 'requestor_email', 'license_title', 'created_at', 'approved_at')


class RejectedRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishRequest
        fields = ('id', 'requestor', 'resource_type', 'language', 'checking_level', 'source_text', 'source_version',
                  'contributors', 'requestor_email', 'license_title', 'created_at', 'rejected_at', 'rejected_by')
        read_only_fields = ('id', 'requestor', 'resource_type', 'language', 'checking_level', 'source_text', 'source_version',
                            'contributors', 'requestor_email', 'license_title', 'created_at', 'rejected_at',
                            'rejected_by')
