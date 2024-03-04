from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from .serializers import ImageHistorySerializer
from rest_framework.response import Response
from .utils import ConvertTextToImage
from .models import ImageHistory
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("hi")

@method_decorator(csrf_exempt, name='dispatch')
class ImageToTextApi(APIView):
    serializer_class=ImageHistorySerializer
    model = ImageHistory

    def get(self, request):
        queryset = self.model.objects.all()
        serizlier = self.serializer_class(queryset, many=True)
        history_id = request.query_params.get('history_id')
        if history_id:
            history_obj=self.model.objects.get(id=history_id)
            serizlier = self.serializer_class(history_obj)
            return Response({"data":serizlier.data})
        return Response(serizlier.data)
    
     
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        saved_id = instance.id
        process = ConvertTextToImage()
        result=process.get_text_from_image(request,saved_id)
        print(result)
        return Response({"data":serializer.data,"text":result})
    
    def delete(self, request):
        history_id = request.query_params.get('history_id')
        if history_id:
            history_obj=self.model.objects.get(id=history_id)
            history_obj.delete()
            return Response({"data":"success"})

