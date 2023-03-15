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
      utterThis.rate = 0.4;
      const voices = synth.getVoices();
      if (voices.length < 2) {
        throw synth;
      }
      utterThis.voice = voices.filter((voice) => voice.lang == "en-US")[0];
      synth.speak(utterThis);
      utterThis.onend = onEnd;
      return synth;
    },
  },
};
