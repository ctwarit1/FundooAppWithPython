from rest_framework import serializers, request

from notes.models import Note, Label
from user.models import User


class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label',
                  'collaborator']
        read_only_fields = ['image', 'label', 'collaborator']

    def create(self, validated_data):
        note = Note.objects.create(**validated_data)
        if self.initial_data.get("collaborator"):
            users = []
            for collaborator in self.initial_data.get("collaborator"):
                try:
                    user = User.objects.get(id=collaborator)
                    users.append(user)
                except collaborator.DoesNotExist:
                    raise Exception(f"{collaborator} not found")
            note.collaborator.add(*users)

        if self.initial_data.get("label"):
            for label in self.initial_data.get("label"):
                try:
                    label = Label.objects.get(name=label, user=validated_data["user"])
                except Label.DoesNotExist:
                    label = Label.objects.create(name=label, user=validated_data["user"])
                note.label.add(label)
        return note


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'user', 'created_at', 'modified_at']
        read_only_fields = ['created_at', 'modified_at']
    def create(self, validated_data):
        label = Label.objects.filter(name=validated_data["name"], user=validated_data["user"])
        if label.exists():
            raise Exception("Label exist")
        label = Label.objects.create(**validated_data)

        return label