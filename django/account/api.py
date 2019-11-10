from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from account.serializers import  RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from account.models import file_storage
from django.core.files.base import ContentFile
from django.forms.models import model_to_dict
from rest_auth.views import LoginView
from .predict_ai import prediction
import numpy as np
import pandas as pd
import os, json

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': model_to_dict(user_token, fields=['id', 'username', 'email']),
        })

class UserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request._user:
            return Response(User.objects.get(pk=request._user.pk))
        else:
            return Response({"Error":"Please Login"})


class FileUploadAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        ab_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ab_path += "/account/checkpoint.pth"

        
        file = request.data['file']
        image_bytes = file.read()
        prob, top_class = prediction(image_bytes)
        top_class = pd.Series(np.asarray(top_class))
        prob = pd.Series(prob)
        DataFrame = pd.DataFrame(dict(Probability = prob, Diagnosed_Diseses = top_class))
        df = DataFrame.to_json(orient = 'records')
#        print(JSON_Response)
        JSON_Response = json.loads(df)

        return Response(JSON_Response)

class GetFilesAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        res = []
        count = 1
        for item in encrypted_storage.objects.filter(user=request.user):
            res.append({count:{"path": item.encrypted_blob.url, "name": item.encrypted_blob.name}})
            count += 1
        return Response(res)
        