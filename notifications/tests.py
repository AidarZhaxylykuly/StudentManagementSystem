from django.test import TestCase
from django.core.cache import cache
from notifications.tasks import send_attendance_reminder, send_grade_update
from unittest.mock import patch
from celery.result import AsyncResult

class CeleryTaskTestCase(TestCase):

    def test_send_attendance_reminder_task(self):
        with patch('notifications.tasks.send_attendance_reminder.apply_async') as mock_task:
            send_attendance_reminder.apply_async()

            mock_task.assert_called_once()

    def test_send_grade_update_task(self):
        with patch('notifications.tasks.send_grade_update.apply_async') as mock_task:
            send_grade_update.apply_async()

            mock_task.assert_called_once()

    def test_send_attendance_reminder_task_result(self):
        with patch('notifications.tasks.send_attendance_reminder') as mock_task:
            mock_task.return_value = 'Success'
            result = send_attendance_reminder.apply_async()

            self.assertEqual(result.result, 'Success')
            self.assertTrue(isinstance(result, AsyncResult))
