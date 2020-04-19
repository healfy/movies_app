from django.http import HttpResponseRedirect
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError


from .models import Movie
from .serializers import MovieSerializer
from .serializers import URLSerializer
from .tasks import download_and_create_video


class MyUploadView(APIView):
    parser_class = (FileUploadParser,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main.html'
    success_url = '/api/v1/index'

    def get(self, request):
        return Response({'movies': Movie.objects.all()})

    def post(self, request, format=None):
        if request.data.get('url') and request.data.get('db_file'):
            raise ValidationError('u cannot upload file from url and file')
        if request.data.get('url'):
            return self.create_from_url(request)
        return self.create_from_file(request)

    def create_from_file(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(redirect_to=self.success_url)
        return Response(
            data={'serializer': serializer, 'errors': serializer.errors})

    def create_from_url(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            download_and_create_video.apply_async(args=(url, ))
            return HttpResponseRedirect(redirect_to=self.success_url)
        return Response(
            data={'serializer': serializer, 'errors': serializer.errors})
