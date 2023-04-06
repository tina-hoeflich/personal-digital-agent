from unittest.mock import patch, MagicMock

from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler

from proaktiv_sender import ProaktivSender
from flask_socketio import SocketIO

from scheduler import Scheduler


@patch.object(BackgroundScheduler, "remove_job")
def test_cancel_all_jobs(mock_remove_jobs):
	job = Job(None)
	job.id = "ID"
	job.name = "NAME"
	with patch.object(BackgroundScheduler, "get_jobs", return_value=[job]) as mock_get_jobs:
		sched = Scheduler()
		sched.cancel_all_jobs()

		mock_remove_jobs.assert_called_once()
		mock_get_jobs.assert_called_once()
