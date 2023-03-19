import os
from django.conf import settings

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, parsers
from rest_framework.response import Response
from storages.backends.s3boto3 import S3Boto3Storage

from attachments.serializers import TaskFileSerializer
from rest_framework import serializers


class UploadIssueAttachmentAPIView(generics.GenericAPIView):
    serializer_class = TaskFileSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)

    @extend_schema(
        responses={201: inline_serializer(
            'AttachmentUpdateStatusSerializer',
            fields={
                'message': serializers.CharField(),
                'fileUrl': serializers.CharField(),
            }
        )},
        description=f"Allowed file size less than or equal to {settings.MAX_UPLOAD_SIZE / (1024 * 1024) } MB"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        file_directory_within_bucket = 'proof_of_work/'
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            data['file'].name
        )

        media_storage = S3Boto3Storage()

        if not media_storage.exists(file_path_within_bucket):  # avoid overwriting existing file
            media_storage.save(file_path_within_bucket, data['file'])
            file_url = media_storage.url(file_path_within_bucket)
            return Response({
                'message': 'OK',
                'fileUrl': file_url,
            }, status=201)
        else:
            return Response({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=data['file'].name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)
