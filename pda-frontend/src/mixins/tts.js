export default {
  data: {
    speechSynthesis: window.speechSynthesis,
    voice: undefined,
  },
  mounted() {
    if (!this.speakingSupported()) {
      console.error("SpeechSynthesis not supported in this browser!");
    } else {
	  this.speechSynthesis.getVoices();
	  speechSynthesis.addEventListener("voiceschanged", () => {
		this.initializeTTS();
	  })
    }
  },
  methods: {
    /**
     * Initialisiert die Sprachausgabe
     */
    initializeTTS() {
      const voices = window.speechSynthesis.getVoices();
      // use nathan voice if available, otherwise use first default voice
      var nathan = voices.filter(
        (voice) => voice.voiceURI == "Nathan (erweitert)"
      )[0];
      var firstDefaultVoice = voices.filter(
        (voice) => voice.lang == "en-US" && voice.default
      )[0];
      this.voice = nathan ?? firstDefaultVoice;
      console.log("Using voice:", this.voice);
    },
    /**
     * Liest einen Text vor
     * @param text der Text der vorgelesen werden soll
     * @param onEnd methode die ausgeführt wird nach Ende des Vorlesens
     */
    speakString(text, onEnd) {
      const utterThis = new SpeechSynthesisUtterance(text);
      utterThis.pitch = 1;
      utterThis.rate = 0.8;
      utterThis.voice = this.voice;
      speechSynthesis.speak(utterThis);
      utterThis.onend = onEnd;
    },
    /**
     * Prüft ob die Sprachausgabe unterstützt wird
     * @returns true wenn Sprachausgabe unterstützt wird, sonst false
     */
    speakingSupported() {
      return window.speechSynthesis != undefined;
    },
  },
};
