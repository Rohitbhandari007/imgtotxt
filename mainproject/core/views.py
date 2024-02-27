from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from .serializers import ImageHistorySerializer
from rest_framework.response import Response
from .utils import ConvertTextToImage
from .models import ImageHistory

def index(request):
    return HttpResponse("hi")


class ImageToTextApi(APIView):
    serializer_class=ImageHistorySerializer
    model = ImageHistory

    def get(self, request):
        queryset = self.model.objects.all()
        serizlier = self.serializer_class(queryset, many=True)
        return Response(serizlier.data)
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        saved_id = instance.id
        process = ConvertTextToImage()
        result = process.get_text_from_image(request,saved_id)
        if result is not None:
            return Response(serializer.data)
        else:
            return Response("Something went wrong")


