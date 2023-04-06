from unittest.mock import patch, MagicMock
from proaktiv_sender import ProaktivSender
from flask_socketio import SocketIO


@patch.object(SocketIO, "emit")
def test_send_socketio(mock_socketemit):
	sender = ProaktivSender(SocketIO())
	sender.send_text("TESTING")
	assert "proaktiv" in mock_socketemit.call_args.args
	assert {'text': 'TESTING'} in mock_socketemit.call_args.args

