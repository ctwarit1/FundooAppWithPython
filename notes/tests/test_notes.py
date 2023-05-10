import json

import pytest
from rest_framework.reverse import reverse


@pytest.fixture()
def login_user(client, django_user_model):
    user_data = {
        "first_name": "twarit",
        "last_name": "chokniwal",
        "username": "kajri",
        "email": "ctwarit1@gmail.com",
        "password": "00000",
        "location": "kota",
        "phone": "7777777",
        "is_verified": True,
    }
    url = reverse('UserReg')
    response = client.post(url, user_data)
    login_data = {
        "username": "kajri",
        "password": "00000"
    }
    url = reverse('UserLogin')
    response = client.post(url, login_data)
    return response.data.get("data")


class TestNotes:

    #                                      successful test cases
    #                                successful test case for create note

    @pytest.mark.django_db
    def test_create_note_successful(self, client, django_user_model, login_user):
        """Test for create note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    #                                successful test case for update note

    @pytest.mark.django_db
    def test_update_note_successful(self, client, django_user_model, login_user):
        """Test for update note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        update_note = {
            "id": note_id,
            "title": "hello",
            "description": "good morning",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.put(url, update_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                successful test case for get note

    @pytest.mark.django_db
    def test_get_note_successful(self, client, django_user_model, login_user):
        """Test for get note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        get_note = {
            "id": note_id,
        }
        url = reverse('notes')
        response = client.get(url, get_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                successful test case for delete note

    @pytest.mark.django_db
    def test_delete_note_successful(self, client, django_user_model, login_user):
        """Test for delete note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        delete_note = {
            "id": note_id,
        }
        url = reverse('notes')
        response = client.delete(url, delete_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 204

    #                                    failure test case Notes
    #                                failure test case for create note

    @pytest.mark.django_db
    def test_create_note_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for create note"""
        token = login_user
        create_note = {
            "title": "",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    #                                failure test case for update note

    @pytest.mark.django_db
    def test_update_note_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for update note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        update_note = {
            "id": note_id,
            "title": "",
            "description": "good morning",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.put(url, update_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    #                                failure test case for get note

    @pytest.mark.django_db
    def test_get_note_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for get note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good morning",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        get_note = {
        }
        url = reverse('notes')
        response = client.get(url, get_note, content_type='application/json')
        assert response.status_code == 400

    #                                failure test case for delete note

    @pytest.mark.django_db
    def test_delete_note_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for delete note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        delete_note = {
            "id": "",
        }
        url = reverse('notes')
        response = client.delete(url, delete_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400


class TestLabels:

    #                                successful test case for create label

    @pytest.mark.django_db
    def test_create_label_successful(self, client, django_user_model, login_user):
        """Test for create label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    #                                successful test case for update label

    @pytest.mark.django_db
    def test_update_label_successful(self, client, django_user_model, login_user):
        """Test for update label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        update_label = {
            "id": note_id,
            "name": "chokniwal"
        }
        url = reverse('label')
        response = client.put(url, update_label, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    #                                successful test case for get label

    @pytest.mark.django_db
    def test_get_label_successful(self, client, django_user_model, login_user):
        """Test for get label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        get_label = {
            "id": note_id,
        }
        url = reverse('label')
        response = client.get(url, get_label, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                successful test case for delete label

    @pytest.mark.django_db
    def test_delete_label_successful(self, client, django_user_model, login_user):
        """Test for delete label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        delete_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.delete(url, delete_label, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                           failure test cases for labels

    @pytest.mark.django_db
    def test_create_label_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for create label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": ""
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update_label_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for update label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        update_label = {
            "id": note_id,
            "name": ""
        }
        url = reverse('label')
        response = client.put(url, update_label, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_label_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for get label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        get_label = {
            "id": note_id,
            "name": ""
        }
        url = reverse('label')
        response = client.get(url, get_label, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_label_unsuccessful(self, client, django_user_model, login_user):
        """Failure Test for delete label"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        delete_label = {
            "id": note_id,
            "name": ""
        }
        url = reverse('label')
        response = client.delete(url, delete_label, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    #                                         successful test cases for archive note

    @pytest.mark.django_db
    def test_post_archive_note(self, client, django_user_model, login_user):
        """Test for post Archive note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        archive_note = {
            "id": note_id,
            "isArchive": True
        }
        url = reverse('is_archive')
        response = client.post(url, archive_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_get_archive_note(self, client, django_user_model, login_user):
        """Test for get Archive note"""

        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        archive_note = {
        }
        url = reverse('is_archive')
        response = client.get(url, archive_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                         successful test cases for trash note

    @pytest.mark.django_db
    def test_post_trash_note(self, client, django_user_model, login_user):
        """Test for post Trash note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        trash_note = {
            "id": note_id,
            "isTrash": True
        }
        url = reverse('is_trash')
        response = client.post(url, trash_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_get_trash_note(self, client, django_user_model, login_user):
        """Test for get Trash note"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        trash_note = {
        }
        url = reverse('is_trash')
        response = client.get(url, trash_note, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                           Test cases for Labels with notes

    #                                        Success Test Case for label with notes

    @pytest.mark.django_db
    def test_post_label_with_notes(self, client, django_user_model, login_user):
        """Test for post label with notes"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        create_label_notes = {
            "id": note_id,
            "name": ["twarit"]
        }
        url = reverse('label_with_notes')
        response = client.post(url, create_label_notes, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_delete_label_with_notes(self, client, django_user_model, login_user):
        """Test for delete label with notes"""

        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        delete_label_notes = {
            "id": note_id,
            "name": "twarit"
        }
        url = reverse('label_with_notes')
        response = client.delete(url, delete_label_notes, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                                        Failure Test Case for label with notes

    @pytest.mark.django_db
    def test_post_label_notes_failure(self, client, django_user_model, login_user):
        """Failure Test for post label with notes"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        create_label_notes = {
            "id": note_id
        }
        url = reverse('label_with_notes')
        response = client.post(url, create_label_notes, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_label_notes_failure(self, client, django_user_model, login_user):
        """Failure Test for delete label with notes"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        create_label = {
            "name": "twarit"
        }
        url = reverse('label')
        response = client.post(url, create_label, HTTP_TOKEN=token, content_type='application/json')
        delete_label_notes = {
            "name": "twarit"
        }
        url = reverse('label_with_notes')
        response = client.delete(url, delete_label_notes, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    #                               Success test cases for collab with notes

    @pytest.mark.django_db
    def test_post_collab_with_notes(self, client, django_user_model, login_user):
        """Test for post collab with notes"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        user_id = response.data["data"]["user"]
        create_collab = {
            "id": note_id,
            "collaborator": [user_id]
        }
        url = reverse('collab_with_notes')
        response = client.post(url, create_collab, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_delete_collab_with_notes(self, client, django_user_model, login_user):
        """Test for delete collab with notes"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        user_id = response.data["data"]["user"]
        delete_collab = {
            "id": note_id,
            "collaborator": [user_id]
        }
        url = reverse('collab_with_notes')
        response = client.delete(url, delete_collab, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 200

    #                       Failure test cases for collab with notes

    @pytest.mark.django_db
    def test_post_collab_with_failure(self, client, django_user_model, login_user):
        """Failure Test for post collab with notes"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        user_id = response.data["data"]["user"]
        create_collab = {
            "collaborator": [user_id]
        }
        url = reverse('collab_with_notes')
        response = client.post(url, create_collab, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_collab_with_failure(self, client, django_user_model, login_user):
        """Failure Test for delete collab with notes"""
        token = login_user
        create_note = {
            "title": "hi",
            "description": "good",
            "color": "blue"
        }
        url = reverse('notes')
        response = client.post(url, create_note, HTTP_TOKEN=token, content_type='application/json')
        note_id = response.data["data"]["id"]
        user_id = response.data["data"]["user"]
        delete_collab = {
            "id": note_id
        }
        url = reverse('collab_with_notes')
        response = client.delete(url, delete_collab, HTTP_TOKEN=token, content_type='application/json')
        assert response.status_code == 400
