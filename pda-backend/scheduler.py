from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job
from typing import Callable

class Scheduler:
	sched: BackgroundScheduler = None
	DISABLED = True
	def __init__(self):
		"""Initialize the scheduler."""
		print("Initializing scheduler...")

		self.sched = BackgroundScheduler()
		self.sched.start()

		print("Scheduler initialized!")

	def schedule_job(self, function: Callable, run_datetime: datetime) -> Job:
		"""Schedule a job to run on a background thread."""
		if self.DISABLED:
			print("DISABLED SCHEDULER!")
			return None
		print(f"Scheduling job '{function.__qualname__}' for execution at {str(run_datetime)}")

		trigger = CronTrigger(day=run_datetime.day, month=run_datetime.month, year=run_datetime.year, hour=run_datetime.hour, minute=run_datetime.minute, second=run_datetime.second, timezone="Europe/Berlin")
		job = self.sched.add_job(function, trigger)
		return job

	def cancel_all_jobs(self):
		"""Cancel all scheduled jobs."""
		print("Cancelling all scheduled jobs...")
		for job in self.sched.get_jobs():
			print(f"Canceling job with id {job.id} and name {job.name}")
			self.sched.remove_job(job.id)
