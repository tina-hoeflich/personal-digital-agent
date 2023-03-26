export default {
	data: {
		speechRecognition: new window.webkitSpeechRecognition(),
	},

	mounted() {
		if (!this.listeningSupported()) {
			alert("SpeechRecognition not supported in this browser!");
		} else {
			this.initializeSTT();
		}
	},

	methods: {
		/**
		 * Initialisiert die Spracherkennung
		 */
		initializeSTT() {
			this.speechRecognition.continuous = false;
  		this.speechRecognition.interimResults = true;
			this.speechRecognition.lang = "en-US";
			this.speechRecognition.onstart = () => console.log("Started Listening");
			this.speechRecognition.onend = () => console.log("Ended Listening");
			this.speechRecognition.onerror = (event) => console.log("Error listening", event.error, event.message);
		},

		/**
		 * Prüft ob die Spracherkennung unterstützt wird
		 * @returns true wenn Spracherkennung unterstützt wird, sonst false
		 */
		listeningSupported() {
			return window.webkitSpeechRecognition != undefined;
		}
	}
}
