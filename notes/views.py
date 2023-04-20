import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from user.utils import authenticate_user
from logger import logger
from notes.models import Note
from notes.serializers import NoteSerializers


# Create your views here.
class CreateNote(APIView):

    @authenticate_user
    def post(self, request):
        try:
            serializer = NoteSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Notes Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def get(self, request):
        try:
            notes = Note.objects.filter(user_id=request.data.get("user"), isArchive=False, isTrash=False)
            serializer = NoteSerializers(notes, many=True)
            return Response({"message": "Note Fetched", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
    @authenticate_user
    def put(self, request):
        try:
            notes = Note.objects.get(user_id=request.data.get("user"), id=request.data.get("id"))
            serializer = NoteSerializers(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Note Updated", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def delete(self, request):
        try:
            notes = Note.objects.filter(user_id=request.data.get("user"), id=request.data.get("id"))

            notes.delete()
            return Response({"message": "Note Deleted", "status": 204},
                            status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class Archive(APIView):
    def post(self, request):
        try:
            notes = Note.objects.get(user_id=request.data.get("user"), id=request.data.get("id"))
            notes.isArchive = True if not notes.isArchive else False
            notes.save()
            return Response({"message": "Note is Archived", "status": 202},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            notes = Note.objects.filter(user_id=request.data.get("user"), isArchive=True, isTrash=False)
            serializer = NoteSerializers(notes, many=True)
            return Response({"message": "Note Fetched", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class Trash(APIView):
    def post(self, request):
        try:
            notes = Note.objects.get(user_id=request.data.get("user"), id=request.data.get("id"))
            notes.isTrash = True if not notes.isTrash else False
            notes.save()
            return Response({"message": "Note is in Trash", "status": 202},
                            status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            notes = Note.objects.filter(user_id=request.data.get("user"), isArchive=False, isTrash=True)
            serializer = NoteSerializers(notes, many=True)
            return Response({"message": "Note Fetched", "status": 200, "data": serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
