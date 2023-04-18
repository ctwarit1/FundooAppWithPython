import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import Note
from notes.serializers import NoteSerializers


# Create your views here.
class CreateNote(APIView):

    def post(self, request):
        try:
            serializer = NoteSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Notes Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)})

    def get(self, request):
        try:
            notes = Note.objects.filter(user_id=request.data.get("user"), isArchive=False, isTrash=False)
            serializer = NoteSerializers(notes, many=True)
            return Response({"message": "Note Fetched", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)})

    def put(self, request):
        try:
            notes = Note.objects.get(user_id=request.data.get("user"), id=request.data.get("id"))
            serializer = NoteSerializers(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Note Updated", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)})

    def delete(self, request):
        try:
            notes = Note.objects.filter(user_id=request.data.get("user"))
            if not notes:
                return Response({"message": "Invalid ID"})

            notes.delete()
            return Response({"message": "Note Deleted", "status": 204},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)})


