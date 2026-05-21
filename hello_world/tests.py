from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Story, Comment


class AuthViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    # --------------------
    # LOGIN
    # --------------------
    def test_login_get(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_post_valid(self):
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "password123"}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_post_invalid(self):
        response = self.client.post(
            "/login/", {"username": "wrong", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 200)

    # --------------------
    # SIGNUP
    # --------------------
    def test_signup_get(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)


class LogoutViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_logout_get(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 200)

    def test_logout_post(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post("/logout/")
        self.assertEqual(response.status_code, 302)


class MeetupsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_meetups_get(self):
        response = self.client.get("/meetups/")
        self.assertEqual(response.status_code, 200)

    def test_meetups_post_not_logged_in(self):
        response = self.client.post("/meetups/", {"trip": "surf1"})
        self.assertEqual(response.status_code, 302)

    def test_meetups_post_logged_in(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post("/meetups/", {"trip": "surf1"})
        self.assertEqual(response.status_code, 302)


class StoryViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        self.story = Story.objects.create(
            title="Test Story",
            author="Author",
            content="Content",
            author_user=self.user,
        )

    # --------------------
    # STORIES PAGE
    # --------------------
    def test_stories_get(self):
        response = self.client.get("/stories/")
        self.assertEqual(response.status_code, 200)

    def test_stories_post_not_logged_in(self):
        response = self.client.post(
            "/stories/", {"story_type": "test_static", "comment": "hello"}
        )
        self.assertEqual(response.status_code, 302)

    def test_stories_post_static_comment(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            "/stories/", {"story_type": "rob_static", "comment": "nice story"}
        )
        self.assertEqual(response.status_code, 302)

    def test_stories_post_dynamic_comment(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            "/stories/", {"story_id": self.story.id, "comment": "great story"}
        )
        self.assertEqual(response.status_code, 302)

    def test_stories_post_invalid_story(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post("/stories/", {"story_id": 99999, "comment": "test"})
        self.assertEqual(response.status_code, 404)


class StoryCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        self.other_user = User.objects.create_user(
            username="other", password="password123"
        )

        self.story = Story.objects.create(
            title="Story", author="Author", content="Content", author_user=self.user
        )

    # --------------------
    # CREATE STORY
    # --------------------
    def test_create_story_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get("/stories/create/")
        self.assertEqual(response.status_code, 200)

    def test_create_story_post(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            "/stories/create/", {"title": "New", "author": "Me", "content": "Hello"}
        )
        self.assertEqual(response.status_code, 302)

    # --------------------
    # EDIT STORY
    # --------------------
    def test_edit_story_permission_denied(self):
        self.client.login(username="other", password="password123")
        response = self.client.get(f"/stories/{self.story.id}/edit/")
        self.assertEqual(response.status_code, 302)

    def test_edit_story_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(f"/stories/{self.story.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_edit_story_post(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            f"/stories/{self.story.id}/edit/",
            {"title": "Updated", "content": "Updated content"},
        )
        self.assertEqual(response.status_code, 302)

    # --------------------
    # DELETE STORY
    # --------------------
    def test_delete_story_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(f"/stories/{self.story.id}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_delete_story_post(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(f"/stories/{self.story.id}/delete/")
        self.assertEqual(response.status_code, 302)


class CommentCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        self.story = Story.objects.create(
            title="Story", author="Author", content="Content", author_user=self.user
        )

        self.comment = Comment.objects.create(
            story=self.story, user=self.user, content="Nice"
        )

    # --------------------
    # EDIT COMMENT
    # --------------------
    def test_edit_comment_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(f"/comments/{self.comment.id}/edit/")
        self.assertEqual(response.status_code, 200)

    def test_edit_comment_post(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            f"/comments/{self.comment.id}/edit/", {"content": "Updated"}
        )
        self.assertEqual(response.status_code, 302)

    # --------------------
    # DELETE COMMENT
    # --------------------
    def test_delete_comment_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(f"/comments/{self.comment.id}/delete/")
        self.assertEqual(response.status_code, 200)

    def test_delete_comment_post(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.post(f"/comments/{self.comment.id}/delete/")
        self.assertEqual(response.status_code, 302)
