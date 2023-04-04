from flask import request, Blueprint, current_app as app
from flask_socketio import SocketIO

class ProaktivSender:
	def __init__(self, socketio: SocketIO):
		self.socketio = socketio

	def send_text(self, text: str):
		"""Send a text to the frontend via socketio

		Args:
			text (str): text to send to the frontend
		"""
		data = {'text': text}
		self.socketio.emit('proaktiv', data)
