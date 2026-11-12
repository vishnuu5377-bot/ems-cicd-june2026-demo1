from rest_framework import filters

from django.shortcuts import render
from.models import Project, UserDetails, employee,department
from rest_framework import viewsets
from .serializers import DepartmentSerializer, EmployeeSerializer, LoginSerializer, ProjectSerializer, UserDetailsSerializer, UserSerializer,Signupserializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate  

# Create your views here.
# EmployeeViewSet------> class name
# viewsets.ModelViewSet--->DRF class that provides default implementations for CRUD operations.
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Allow any user (authenticated or not) to access this view
    # collection of objects from database using ORM
    queryset = employee.objects.all()
    serializer_class = EmployeeSerializer  
    # use the SearchFilter backend to enable search functionality   
    # searchfilter is a built in function provided by django
    filter_backends = [filters.SearchFilter] 
    # specifies the fields in which the search should be performed
    
    search_fields = ['employeename', 'designation']  # Specify the fields to search on
     
    
    
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = department.objects.all()
    serializer_class = DepartmentSerializer 
    
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer    
    
    
# class - based API-APIView is provided by DRF
class SignupAPIView(APIView):
    permission_classes = [AllowAny]  # Allow any user (authenticated or not) to access this view
    
    def post(self, request):
        serializer = Signupserializer(data=request.data)
        if serializer.is_valid():
            # IF THE VALIDATION SUCCESS it will create a new user
            # DRF internally calls create() inside the serializer
            user = serializer.save()
            # if token exists,returns the existing token.otherwise creates a new token for the user
            # token,created=Token.objects.get_or_create(user=user)
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "user_id": user.id,
                "username": user.username,
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                # "token": token.key,
                "role":user.groups.all()[0].id if user.groups.exists() else None
            },status=status.HTTP_201_CREATED)
        else:
            res={'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors} 
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:
                refresh=RefreshToken.for_user(user)

                # token = Token.objects.get(user=user)

                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "username": user.username,
                    "access":str(refresh.access_token),
                    "refresh":str(refresh),
                    # "token": token.key,
                    "role": user.groups.all()[0].id
                    if user.groups.exists() else None
                }

                return Response(
                    response,
                    status=status.HTTP_200_OK
                )

            else:

                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or password"
                }

                return Response(
                    response,
                    status=status.HTTP_401_UNAUTHORIZED
                )

        else:

            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "data": serializer.errors
            }

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )