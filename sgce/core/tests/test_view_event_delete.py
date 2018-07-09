import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import resolve_url as r

from sgce.accounts.models import Profile
from sgce.core.forms import EventForm
from sgce.core.models import Event
from sgce.core.tests.base import LoggedInTestCase


class EventDeleteWithoutPermission(LoggedInTestCase):
    def setUp(self):
        super(EventDeleteWithoutPermission, self).setUp()
        another_user = get_user_model().objects.create_user(username='another_user', password='password')
        self.event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=another_user,
        )
        self.response = self.client.get(r('core:event-delete', self.event.pk))

    def test_get(self):
        """Must return 403 HttpError (No permission)"""
        self.assertEqual(403, self.response.status_code)


#class Base. Add user as MANAGER
class Base(LoggedInTestCase):
    def setUp(self):
        super(Base, self).setUp()
        self.event = Event.objects.create(
            name='Simpósio Brasileiro de Informática',
            start_date=datetime.date(2018, 6, 18),
            end_date=datetime.date(2018, 6, 18),
            location='IFAL - Campus Arapiraca',
            created_by=self.user_logged_in,
        )


class EventDeleteGet(Base):
    def setUp(self):
        super(EventDeleteGet, self).setUp()
        self.response = self.client.get(r('core:event-delete', self.event.pk))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/event/event_check_delete.html')

    def test_html(self):
        """Html must contain input tags"""
        tags = (
            ('<form', 1),
            # CSRF, Name, Start_date, End_date and Location
            ('<input', 1),
            ('type="submit"', 1),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """HTML must contains csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class EventDeletePost(Base):
    def setUp(self):
        super(EventDeletePost, self).setUp()
        self.response = self.client.post(r('core:event-delete', self.event.pk))

    def test_post(self):
        """ Valid POST should redirect to 'user-list' """
        self.assertRedirects(self.response, r('core:event-list'))

    def test_save_user(self):
        self.assertFalse(Event.objects.exists())