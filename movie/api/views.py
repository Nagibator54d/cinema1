from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from movie.models import Movie ,Comment
from .serializers import MovieSerializer,CommentSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404



class MovieListView(GenericAPIView,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,):

    queryset=Movie.objects.all()
    serializer_class=MovieSerializer           

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)


    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class MovieDetailView(GenericAPIView,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin):

    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)           
    
    
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)           

     
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)      















class MovieViewSet(ViewSet):

    queryset=Movie.objects.all()

    def list(self,request):
       serializer=MovieSerializer(self.queryset, many=True)

       return Response(serializer.data, status=HTTP_200_OK)

    def retrieve(self, request, pk=None):
        movie=get_object_or_404(self.queryset, pk=pk)
        serializer= MovieSerializer(movie)

        return Response(serializer.data, status=HTTP_200_OK)

    def create(self,request):
        serializer=MovieSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

    def update(self,request, pk=None):
        movie=get_object_or_404(self.queryset, pk=pk)
        serializer=MovieSerializer(movie, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        movie=get_object_or_404(self.queryset, pk=pk)
        serializer=MovieSerializer(movie,data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=HTTP_403_FORBIDDEN )

    def destroy(self, request, pk=None):
        movie=get_object_or_404(self.queryset,pk=pk)
        movie.delete()
        return Response(status=HTTP_204_NO_CONTENT)    
        
