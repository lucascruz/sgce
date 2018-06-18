from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url as r
from sgce.core.models import Profile
from sgce.core.tests.base import LoggedInTestCase


class UserActiveOrDisablePermission(LoggedInTestCase):
    def setUp(self):
        super(UserActiveOrDisablePermission, self).setUp()
        self.user = get_user_model().objects.create_user(
            username='user_without_permission',
            password='password',
        )
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))

    def test_get_without_permission(self):
        """Must return 403 HttpError (No permission)"""
        self.assertRaises(PermissionDenied)

    def test_get_with_permission(self):
        """Must redirect to core:user-list"""
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Permission

        content_type = ContentType.objects.get_for_model(Profile)
        permission = Permission.objects.get(
            codename='can_enable_or_disable_user',
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)
        self.user.refresh_from_db()

        # user created on LoggedInTestCase setUp()
        first_user = get_user_model().objects.get(pk=1)

        self.response = self.client.get(r('core:user-active-or-disable', first_user.pk))

        self.assertEqual(302, self.response.status_code)


class UserActiveOrDisable(LoggedInTestCase):
    def setUp(self):
        super(UserActiveOrDisable, self).setUp()
        # user created on LoggedInTestCase setUp()
        self.user = get_user_model().objects.get(pk=1)
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))

    def test_get(self):
        """Must redirect to core:user-list"""
        self.assertEqual(302, self.response.status_code)


class UserDisableGet(LoggedInTestCase):
    def setUp(self):
        super(UserDisableGet, self).setUp()
        self.user = get_user_model().objects.create_user(username='user_enable', password='password')
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))
        self.user.refresh_from_db()

    def test_user_has_been_disabled(self):
        self.assertFalse(self.user.is_active)


class UserEnableGet(LoggedInTestCase):
    def setUp(self):
        super(UserEnableGet, self).setUp()
        self.user = get_user_model().objects.create_user(username='user_enable', password='password', is_active=False)
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))
        self.user.refresh_from_db()

    def test_user_has_been_enable(self):
        self.assertTrue(self.user.is_active)


class UserActiveOrDisableHimSelf(LoggedInTestCase):
    def setUp(self):
        super(UserActiveOrDisableHimSelf, self).setUp()
        # user created on LoggedInTestCase setUp()
        self.user = get_user_model().objects.get(pk=1)
        self.response = self.client.get(r('core:user-active-or-disable', self.user.pk))
        self.user.refresh_from_db()

    def test_user_wont_be_disabled(self):
        """The user cannot be himself."""
        self.assertTrue(self.user.is_active)