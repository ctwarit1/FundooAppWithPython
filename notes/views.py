import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from notes.utils import RedisManager
from user.models import User
from user.utils import authenticate_user
from logger import logger
from .models import Note, Label
from notes.serializers import NoteSerializers, LabelSerializer
from django.db.models import Q


# Create your views here.
class CreateNote(APIView):
    """ CRUD operations - NOTES """

    @authenticate_user
    def post(self, request):
        try:
            serializer = NoteSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            RedisManager().save(user_id=request.data.get("user"), notes=serializer.data)
            return Response({"message": "Notes Created", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def get(self, request):
        try:
            redis_dict = RedisManager().get(user_id=request.data.get("user"))
            if redis_dict:
                return Response({"message": "Note Fetched", "status": 200, "data": redis_dict},
                                status=status.HTTP_200_OK)
            notes = Note.objects.filter(Q(user_id=request.data.get("user"), isArchive=False, isTrash=False) |
                                        Q(collaborator__id=request.data.get("user"))).distinct("id")
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
            RedisManager().save(user_id=request.data.get("user"), notes=serializer.data)
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
            RedisManager().delete(user_id=request.data.get("user"), note_id=request.data.get("id"))
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


class Labels(APIView):
    """ CRUD operations - LABEL """

    @authenticate_user
    def post(self, request):
        try:
            serializer = LabelSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Label Added Successfully", "data": serializer.data, "status": 201},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def get(self, request):
        try:
            # label = Label.objects.filter(name=request.data.get("name"))
            label = Label.objects.filter(user_id=request.data.get("user"))
            serializer = LabelSerializer(label, many=True)
            if not label:
                raise Exception("Please enter a valid name")

            return Response({"message": "Label Fetched ", "data": serializer.data, "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def put(self, request):
        try:
            label = Label.objects.get(user_id=request.data.get("user"))
            serializer = LabelSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            if not label:
                raise Exception("Please enter a valid ID")

            serializer.save()
            return Response({"message": "Labels Updated", "data": serializer.data, "status": 201},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def delete(self, request):
        try:
            label = Label.objects.get(name=request.data.get("name"))
            if not label:
                raise Exception("Please enter a valid name")
            label.delete()
            return Response({"message": "Label is Deleted", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class LabelWithNotes(APIView):
    """ Post and Delete Label """

    @authenticate_user
    def post(self, request):
        try:
            note = Note.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            labels = []
            for i in request.data.get("name"):
                try:
                    label = Label.objects.get(name=i, user_id=request.data.get("user"))
                    labels.append(label)
                except Label.DoesNotExist:
                    raise Exception(f"{i} not exist")
            note.label.add(*labels)
            return Response({"message": "Notes with Label Created", "status": 201, "data": {}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def delete(self, request):
        try:
            note = Note.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            label = Label.objects.get(name=request.data.get("name"), user_id=request.data.get("user"))
            note.label.remove(label)

            return Response({"message": "Label is Removed", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)


class CollaboratorWithNotes(APIView):
    """ Post and Delete Label """

    @authenticate_user
    def post(self, request):
        try:
            note = Note.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            collaborators = []
            for i in request.data.get("collaborator"):
                try:
                    collaborator = User.objects.get(id=i)
                    collaborators.append(collaborator)
                except User.DoesNotExist:
                    raise Exception(f"{i} not exist")
            note.collaborator.add(*collaborators)
            return Response({"message": "Collaborators Created", "status": 201, "data": {}},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @authenticate_user
    def delete(self, request):
        try:
            note = Note.objects.get(id=request.data.get("id"), user_id=request.data.get("user"))
            for i in request.data.get("collaborator"):
                collaborator = User.objects.get(id=i)
                note.collaborator.remove(collaborator)
            return Response({"message": "Collaborator Removed", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({"message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
