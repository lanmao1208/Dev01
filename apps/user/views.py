from django.contrib.auth.models import User
from rest_framework.views import APIView
# from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.mixins import CreateModelMixin
from .serializers import RegisterSerializer


class UserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class UserMixinView(GenericAPIView, CreateModelMixin):
#     queryset = Tb_Users.objects.all()
#     serializer_class = RegisterSerializer
#     def post(self, request, *args, **kwargs):
#         # CreateModelMixin中的create方法
#         return self.create(request, *args, **kwargs)


class UsernameIsExistedView(APIView):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        # count = user.count()
        one_dict = {
            'username': username,
            'count': count
        }

        return Response(one_dict)


class EmailIsExistedView(APIView):

    def get(self, request, email):
        count = User.objects.filter(email=email).count()
        # count = user.count()
        one_dict = {
            'email': email,
            'count': count
        }

        return Response(one_dict)
