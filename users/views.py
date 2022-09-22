from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import *
from datetime import datetime
from .models import *
def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

@api_view(['POST'])
def login(request):
    serializer=AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.validated_data['user']
        token=Token.objects.get_or_create(user=user)
        
        return Response({'status':'success',
            'userInfo':{
            'id':user.id,
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            },
            'token':token[0].key
            },status=200)
    else:
        return Response({'status':'fail','message':'Invalid username or password'},status=400)
        

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return Response({
            "user_info": serialize_user(user),
            "token": Token.objects.get_or_create(user=user)[0].key
        })


@api_view(['GET'])
def get_user(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_data': serialize_user(user)
        })
    return Response({})

@api_view(['POST'])
def check_in_api(request):
    user=request.user
    check_in=datetime.now()
    if (Attendance.objects.filter(user=user).count()==0):
        if(check_in.hour>=9 and check_in.minute>=1 and check_in.hour<17 ):
            ReviewAttendance.objects.create(user=user,check_in_late=True,day=check_in.date())
        Attendance.objects.create(user=user,check_in=check_in)
        return Response ({'status':'success','message':'Checked in successfully'})
    else:
        record=Attendance.objects.filter(user=user).last()
        if record.check_out==None:
            return Response({'status':'fail','message':'You have not checked out yet'})
        else:
            if(check_in.hour>=9 and check_in.minute>=1 and check_in.hour<17 ):
                ReviewAttendance.objects.create(user=user,check_in_late=True,day=check_in.date())
            Attendance.objects.create(user=user,check_in=check_in)
            return Response ({'status':'success','message':'Checked in successfully'})

@api_view(['POST'])
def check_out_api(request):
    user=request.user
    check_out=datetime.now()
    if (Attendance.objects.filter(user=user).count()==0):
        return Response({'status':'fail','message':'You have not checked in yet'})
    else:
        record=Attendance.objects.filter(user=user).last()
        if record.check_out==None:
            record.check_out=check_out
            record.save()
            
            if (check_out.hour>9 and check_out.hour<17):
                ReviewAttendance.objects.create(user=user,check_out_early=True,day=check_out.date())
            return Response ({'status':'success','message':'Checked out successfully'})
        else:
            return Response({'status':'fail','message':'You have already checked out'})
    
@api_view(['GET'])
def list_check_in(request):
    if (request.user.is_staff):
        attendance_list=Attendance.objects.all()
    else:
        attendance_list=Attendance.objects.filter(user=request.user)
    serializer=AttendanceSerializer(attendance_list,many=True)
    return Response(serializer.data)
