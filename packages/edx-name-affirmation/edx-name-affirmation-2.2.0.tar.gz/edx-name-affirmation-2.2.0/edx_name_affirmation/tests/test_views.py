"""
All tests for edx_name_affirmation views
"""
import json

import ddt

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse

from edx_name_affirmation.api import (
    create_verified_name,
    create_verified_name_config,
    get_verified_name,
    get_verified_name_history,
    should_use_verified_name_for_certs
)
from edx_name_affirmation.models import VerifiedNameConfig
from edx_name_affirmation.statuses import VerifiedNameStatus

from .utils import LoggedInTestCase

User = get_user_model()


class NameAffirmationViewsTestCase(LoggedInTestCase):
    """
    Base test class for Name Affirmation views
    """

    def setUp(self):
        super().setUp()
        # Create a fresh config with default values
        VerifiedNameConfig.objects.create(user=self.user)

    def tearDown(self):
        super().tearDown()
        cache.clear()


@ddt.ddt
class VerifiedNameViewTests(NameAffirmationViewsTestCase):
    """
    Tests for the VerifiedNameView
    """

    VERIFIED_NAME = 'Jonathan Doe'
    PROFILE_NAME = 'Jon Doe'

    OTHER_VERIFIED_NAME = 'Robert Smith'
    OTHER_PROFILE_NAME = 'Bob Smith'

    ATTEMPT_ID = 11111

    def test_verified_name(self):
        verified_name = self._create_verified_name(status=VerifiedNameStatus.APPROVED)

        expected_data = self._get_expected_data(self.user, verified_name)

        response = self.client.get(reverse('edx_name_affirmation:verified_name'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, expected_data)

    def test_verified_name_existing_config(self):
        verified_name = self._create_verified_name()
        create_verified_name_config(self.user, use_verified_name_for_certs=True)
        expected_data = self._get_expected_data(self.user, verified_name, use_verified_name_for_certs=True)

        response = self.client.get(reverse('edx_name_affirmation:verified_name'))
        data = json.loads(response.content.decode('utf-8'))
        self.assertTrue(data, expected_data)

    def test_staff_access_verified_name(self):
        other_user = User(username='other_tester', email='other@test.com')
        other_user.save()
        create_verified_name(other_user, self.VERIFIED_NAME, self.PROFILE_NAME, status=VerifiedNameStatus.APPROVED)

        # check that non staff access returns 403
        response = self.client.get(reverse('edx_name_affirmation:verified_name'), {'username': other_user.username})
        self.assertEqual(response.status_code, 403)

        self.user.is_staff = True
        self.user.save()

        # create verified name
        self._create_verified_name()
        other_user_verified_name = get_verified_name(other_user, is_verified=True)

        # expected data should match the verifiedname from the other user
        expected_data = self._get_expected_data(other_user, other_user_verified_name)

        response = self.client.get(reverse('edx_name_affirmation:verified_name'), {'username': other_user.username})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, expected_data)

    def test_404_if_no_verified_name(self):
        response = self.client.get(reverse('edx_name_affirmation:verified_name'))
        self.assertEqual(response.status_code, 404)

    def test_post_200(self):
        verified_name_data = {
            'username': self.user.username,
            'profile_name': self.PROFILE_NAME,
            'verified_name': self.VERIFIED_NAME,
            'verification_attempt_id': self.ATTEMPT_ID,
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name'),
            verified_name_data
        )
        self.assertEqual(response.status_code, 200)

        created_name = get_verified_name(self.user, is_verified=False)
        self.assertEqual(created_name.user.username, self.user.username)
        self.assertEqual(created_name.profile_name, self.PROFILE_NAME)
        self.assertEqual(created_name.verified_name, self.VERIFIED_NAME)
        self.assertEqual(created_name.verification_attempt_id, self.ATTEMPT_ID)

    def test_post_200_if_staff(self):
        self.user.is_staff = True
        self.user.save()

        other_user = User(username='other_tester', email='other@test.com')
        other_user.save()

        verified_name_data = {
            'username': other_user.username,
            'profile_name': self.PROFILE_NAME,
            'verified_name': self.VERIFIED_NAME,
            'proctored_exam_attempt_id': self.ATTEMPT_ID,
            'status': VerifiedNameStatus.APPROVED.value,
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name'),
            verified_name_data
        )
        self.assertEqual(response.status_code, 200)

        created_name = get_verified_name(other_user, is_verified=True)
        self.assertEqual(created_name.user.username, other_user.username)
        self.assertEqual(created_name.profile_name, self.PROFILE_NAME)
        self.assertEqual(created_name.verified_name, self.VERIFIED_NAME)
        self.assertEqual(created_name.proctored_exam_attempt_id, self.ATTEMPT_ID)

    def test_post_403_non_staff(self):
        other_user = User(username='other_tester', email='other@test.com')
        other_user.save()

        verified_name_data = {
            'username': other_user.username,
            'profile_name': self.PROFILE_NAME,
            'verified_name': self.VERIFIED_NAME,
            'verification_attempt_id': self.ATTEMPT_ID,
            'status': VerifiedNameStatus.APPROVED.value,
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name'),
            verified_name_data
        )
        self.assertEqual(response.status_code, 403)

    @ddt.data('<html>Verified Name</html>', 'https://verifiedname.com')
    def test_post_400_invalid_name(self, verified_name):
        verified_name_data = {
            'username': self.user.username,
            'profile_name': self.PROFILE_NAME,
            'verified_name': verified_name,
            'verification_attempt_id': self.ATTEMPT_ID,
            'status': VerifiedNameStatus.SUBMITTED.value,
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name'),
            verified_name_data
        )
        self.assertEqual(response.status_code, 400)

    def test_post_400_invalid_serializer(self):
        verified_name_data = {
            'username': self.user.username,
            'profile_name': self.PROFILE_NAME,
            'verified_name': self.VERIFIED_NAME,
            'verification_attempt_id': 'xxyz',
            'status': VerifiedNameStatus.APPROVED.value,
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name'),
            verified_name_data
        )
        self.assertEqual(response.status_code, 400)

    def test_post_400_two_attempt_ids(self):
        verified_name_data = {
            'username': self.user.username,
            'profile_name': self.PROFILE_NAME,
            'verified_name': self.VERIFIED_NAME,
            'verification_attempt_id': self.ATTEMPT_ID,
            'proctored_exam_attempt_id': self.ATTEMPT_ID
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name'),
            verified_name_data
        )
        self.assertEqual(response.status_code, 400)

    def _create_verified_name(
        self, verification_attempt_id=None, proctored_exam_attempt_id=None, status=VerifiedNameStatus.PENDING,
    ):
        """
        Create and return a verified name object.
        """
        create_verified_name(
            self.user,
            self.VERIFIED_NAME,
            self.PROFILE_NAME,
            verification_attempt_id,
            proctored_exam_attempt_id,
            status
        )
        return get_verified_name(self.user)

    def _get_expected_data(
        self, user, verified_name_obj,
        use_verified_name_for_certs=False,
    ):
        """
        Create a dictionary of expected data.
        """
        return {
            'created': verified_name_obj.created.isoformat(),
            'username': user.username,
            'verified_name': verified_name_obj.verified_name,
            'profile_name': verified_name_obj.profile_name,
            'verification_attempt_id': verified_name_obj.verification_attempt_id,
            'proctored_exam_attempt_id': verified_name_obj.proctored_exam_attempt_id,
            'status': verified_name_obj.status,
            'use_verified_name_for_certs': use_verified_name_for_certs,
        }


@ddt.ddt
class VerifiedNameHistoryViewTests(NameAffirmationViewsTestCase):
    """
    Tests for the VerifiedNameHistoryView
    """

    def test_get(self):
        verified_name_history = self._create_verified_name_history(self.user)
        expected_response = self._get_expected_response(self.user, verified_name_history)

        response = self.client.get(reverse('edx_name_affirmation:verified_name_history'))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, expected_response)

    def test_get_bools(self):
        verified_name_history = self._create_verified_name_history(self.user)
        expected_response = self._get_expected_response(
            self.user, verified_name_history,
            use_verified_name_for_certs=False
        )

        response = self.client.get(reverse('edx_name_affirmation:verified_name_history'))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, expected_response)

    def test_get_no_data(self):
        expected_response = self._get_expected_response(self.user, [])
        response = self.client.get(reverse('edx_name_affirmation:verified_name_history'))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, expected_response)

    @ddt.data((True, 200), (False, 403))
    @ddt.unpack
    def test_get_staff_access(self, is_staff, expected_response):
        other_user = User(username='other_tester', email='other@test.com')
        other_user.save()

        if is_staff:
            self.user.is_staff = True
            self.user.save()

        response = self.client.get(
            reverse('edx_name_affirmation:verified_name_history'),
            {'username': other_user.username}
        )

        self.assertEqual(response.status_code, expected_response)

    def _create_verified_name_history(self, user):
        """
        Create and return a verified name QuerySet.
        """
        create_verified_name(
            user,
            'Jonathan Doe',
            'Jon Doe',
            verification_attempt_id=123,
            status=VerifiedNameStatus.APPROVED,
        )
        create_verified_name(
            user,
            'Jane Doe',
            'Jane Doe',
            proctored_exam_attempt_id=456,
            status=VerifiedNameStatus.DENIED,
        )
        return get_verified_name_history(user)

    def _get_expected_response(
        self,
        user,
        verified_name_history,
        use_verified_name_for_certs=False
    ):
        """
        Create and return a verified name QuerySet.
        """
        expected_response = {
            'results': [],
            'use_verified_name_for_certs': use_verified_name_for_certs,
        }

        for verified_name_obj in verified_name_history:
            data = {
                'created': verified_name_obj.created.isoformat(),
                'username': user.username,
                'verified_name': verified_name_obj.verified_name,
                'profile_name': verified_name_obj.profile_name,
                'verification_attempt_id': verified_name_obj.verification_attempt_id,
                'proctored_exam_attempt_id': verified_name_obj.proctored_exam_attempt_id,
                'status': verified_name_obj.status
            }
            expected_response['results'].append(data)

        return expected_response


class VerifiedNameConfigViewTests(NameAffirmationViewsTestCase):
    """
    Tests for the VerifiedNameConfigView
    """

    def test_post_201(self):
        config_data = {
            'username': self.user.username,
            'use_verified_name_for_certs': True
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name_config'),
            config_data
        )
        self.assertEqual(response.status_code, 201)

        use_verified_name_for_certs = should_use_verified_name_for_certs(self.user)
        self.assertTrue(use_verified_name_for_certs)

    def test_post_201_missing_field(self):
        initial_config_data = {
            'username': self.user.username,
            'use_verified_name_for_certs': True
        }
        config_data_missing_field = {'username': self.user.username}

        first_response = self.client.post(
            reverse('edx_name_affirmation:verified_name_config'),
            initial_config_data
        )
        second_response = self.client.post(
            reverse('edx_name_affirmation:verified_name_config'),
            config_data_missing_field
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)

        # `use_verified_name_for_certs` should not be overriden with False due to a missing field
        use_verified_name_for_certs = should_use_verified_name_for_certs(self.user)
        self.assertTrue(use_verified_name_for_certs)

    def test_post_201_if_staff(self):
        self.user.is_staff = True
        self.user.save()

        other_user = User(username='other_user', email='other@test.com')
        other_user.save()

        config_data = {
            'username': other_user.username,
            'use_verified_name_for_certs': True
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name_config'),
            config_data
        )
        self.assertEqual(response.status_code, 201)

        use_verified_name_for_certs = should_use_verified_name_for_certs(other_user)
        self.assertTrue(use_verified_name_for_certs)

    def test_post_403_non_staff(self):
        other_user = User(username='other_tester', email='other@test.com')
        other_user.save()

        config_data = {
            'username': other_user.username,
            'use_verified_name_for_certs': True
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name_config'),
            config_data
        )
        self.assertEqual(response.status_code, 403)

    def test_post_400_invalid_serializer(self):
        config_data = {
            'username': self.user.username,
            'use_verified_name_for_certs': 'not a boolean'
        }
        response = self.client.post(
            reverse('edx_name_affirmation:verified_name_config'),
            config_data
        )
        self.assertEqual(response.status_code, 400)
