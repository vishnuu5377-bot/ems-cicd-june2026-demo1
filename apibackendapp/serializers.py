from datetime import date
import re
from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Project, UserDetails, department, employee
from django.contrib.auth.hashers import make_password



def date_of_joining_restriction(dateOfJoining):
    today = date.today()

    if dateOfJoining != today:
        raise serializers.ValidationError(
            "Date of joining must be today."
        )

    return dateOfJoining




def name_validation(employeeName):

    if len(employeeName) < 3:
        raise serializers.ValidationError(
            "Employee name must be at least 3 characters."
        )

    if not re.match("^[A-Za-z ]+$", employeeName):
        raise serializers.ValidationError(
            "Employee name must contain only letters and spaces."
        )

    return employeeName




def designation_validation(designation):

    if len(designation) < 2:
        raise serializers.ValidationError(
            "Designation must be at least 2 characters."
        )

    if not re.match("^[A-Za-z ]+$", designation):
        raise serializers.ValidationError(
            "Designation must contain only letters and spaces."
        )

    return designation




def contact_validation(contact):

    if not contact.isdigit():
        raise serializers.ValidationError(
            "Contact must contain only numbers."
        )

    if len(contact) != 10:
        raise serializers.ValidationError(
            "Contact must be exactly 10 digits."
        )

    return contact




class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = department
        fields = '__all__'




class EmployeeSerializer(serializers.ModelSerializer):

    # Display department details
    Department = DepartmentSerializer(
        source='departmentid',
        read_only=True
    )

    # Date validation
    dateofjoining = serializers.DateField(
        validators=[date_of_joining_restriction]
    )

    # Employee name validation
    employeename = serializers.CharField(
        max_length=100,
        validators=[name_validation]
    )

    # Designation validation
    designation = serializers.CharField(
        max_length=100,
        validators=[designation_validation]
    )

    # Contact validation
    contact = serializers.CharField(
        max_length=10,
        validators=[contact_validation]
    )

    # Display project details
    project_details = serializers.StringRelatedField(
        source='projects',
        many=True,
        read_only=True
    )

    class Meta:

        model = employee

        fields = (
            'employeeid',
            'employeename',
            'designation',
            'dateofjoining',
            'contact',
            'isactive',
            'Department',
            'project_details'
        )



class ProjectSerializer(serializers.ModelSerializer):

    # Display employee details
    employee_details = EmployeeSerializer(
        source='employees',
        required=False,
        many=True,
        read_only=True
    )

    class Meta:

        model = Project

        fields = (
            'id',
            'name',
            'employees',
            'employee_details'
        )
        
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')     
        
        
                     
# receives the registration data,validates it and hashes the password,creates the user
# and assigns the user to a group nad finally returns the created user  
class Signupserializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True,required=False)
    

    def create(self, validated_data):
        group_name = validated_data.pop('group_name', None)
       
 # hash the password before saving the user
        validated_data['password'] = make_password(validated_data['password'])
        user = super(Signupserializer, self).create(validated_data)
        
        
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)          
            
        return user
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'group_name')
        extra_kwargs = {'password': {'write_only': True}}   
        
class LoginSerializer(serializers.Serializer):
    # field to get username fro, user
    username = serializers.CharField()
    # field to get password from user
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model=User
        fields = ('username', 'password')