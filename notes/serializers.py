from rest_framework import serializers

from notes.models import Note


class NoteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label', 'collaborator']
        read_only_fields = ['image', 'label', 'collaborator']

    def create(self, validated_data):
        return Note.objects.create(**validated_data)




