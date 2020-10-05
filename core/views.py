from rest_framework import settings
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer
from .models import UserModel
from rest_framework.response import Response
from django.conf import settings
from .tasks import GetCountAndResourcesDone

class GetAllUserList(APIView):
    def get(self,request):
        query = UserModel.objects.all()
        serializer = UserSerializer(query,many=True)
        serializer_data = sorted(serializer.data, key = lambda i: i['quests_status'],reverse=True)[0:20]
        return Response(serializer_data,status=200)

    def post(self,request):
        req_data = request.data
        data = GetCountAndResourcesDone(req_data['link'])
        user = UserModel()
        user.qwiklabs_id = req_data['link']
        user.quests_status = len(data['quests'])
        user.quests = data['quests']
        user.name = data['name']
        user.dp = data['dp']
        user.save()
        return Response(status=204)