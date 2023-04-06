from unittest.mock import patch

from sendgrid import SendGridAPIClient

import services.email_service as email_service


@patch.object(SendGridAPIClient, "send", return_value={"type": "single", "joke": "I am funny!"})
def test_mail(send_mock):
	mail = email_service.send_email("sender", "recipiant", "subject", "content")
	assert "subject" in mail.subject.subject

	send_mock.assert_called_once()
