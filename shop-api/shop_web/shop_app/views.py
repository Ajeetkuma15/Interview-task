

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from rest_framework.decorators import api_view,permission_classes,authentication_classes,parser_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import ShopLocation

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
    



class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
    

@api_view(['GET','POST'])
@parser_classes([MultiPartParser,FormParser,JSONParser])
@permission_classes([IsAuthenticated])
# @authentication_classes(CsrfExemptSessionAuthentication, BasicAuthentication)

def shoplocation_list(request, format=None):
    if request.method == 'POST':
        serializers = ShopSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response({'data':serializers.errors, 'status':True, 'message':"fail"},status=400)
    
    elif request.method == 'GET':
        paginator = PageNumberPagination()
        snippets = ShopLocation.objects.all()
        snippets = paginator.paginate_queryset(snippets, request)
        serializers = GetshopSerializer(snippets, many=True)
        return Response(serializers.data)
    
@api_view(['GET','PUT','DELETE'])
@parser_classes([MultiPartParser,FormParser,JSONParser])
@permission_classes([IsAuthenticated])
def shop_details(request, pk, format=None):
    try:
        shop_details =  ShopLocation.objects.get(pk=pk)
    except ShopLocation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    if request.method == 'GET':
        serializers = GetshopSerializer(shop_details)
        print(serializers.data)
        return JsonResponse({'data':serializers.data,'status':True,'message':"success"},  status=200)
    

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = ShopSerializer(shop_details, data=data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return JsonResponse({'data':serializers.data,'status':True,'message':"success"}, status=201)
        return JsonResponse({'data':serializers.errors,'status':True,'message':"success"}, status=400)

    elif request.method == 'DELETE':
        try:
            shop_details.delete()
            return Response({'data':{},'status':True,'message':"Deleted success"},status=200)
        except:
            return Response({'data':{},'status':False,'message':"Product Type Attched with Someone"},status=403)

    
