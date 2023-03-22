export default {
  methods: {
    /**
     * Liest einen Text vor
     * @param text der Text der vorgelesen werden soll
     * @param onEnd methode die ausgeführt wird nach Ende des Vorlesens
     * @returns das SpeechSynthesis Objekt
     */
    speakString(text, onEnd) {
      const synth = window.speechSynthesis;
      const utterThis = new SpeechSynthesisUtterance(text);
      utterThis.pitch = 1;
      utterThis.rate = 0.8;
      const voices = synth.getVoices();
      if (voices.length < 2) {
        throw synth;
      }
			// use nathan voice if available, otherwise use first default voice
      var nathan = voices.filter((voice) => voice.voiceURI == "Nathan (erweitert)")[0];
			var firstDefaultVoice = voices.filter((voice) => voice.default)[0];
			utterThis.voice = nathan ?? firstDefaultVoice;
      console.log("Using voice:", utterThis.voice)
      synth.speak(utterThis);
      utterThis.onend = onEnd;
      return synth;
    },
  },
};
