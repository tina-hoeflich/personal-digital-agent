<template>
  <div @click="animate()" style="height: 400px">
    <v-img
      v-if="speaking || listening"
      contain
      src="@/assets/circles_spinning.gif"
      max-height="400px"
    />
    <v-img v-else contain src="@/assets/frame_0.png" max-height="400px" />
  </div>
  <h1 v-html="jarvisText"></h1>
  <v-row align="center" justify="center">
    <v-col cols="11">
      <v-textarea
        clearable
        prepend-icon="mdi-microphone-message"
        variant="outlined"
        label="Eingabe"
        rows="2"
        v-model="userText"
        :readonly="listening"
				@keydown.enter.prevent="send2Jarvis"
      ></v-textarea>
    </v-col>
    <v-col cols="1">
      <v-btn
        icon="mdi-microphone"
        color="primary"
        size="x-large"
        :active="listening"
        @click="startStopListening()"
      ></v-btn>
    </v-col>
  </v-row>
  <v-btn size="large" color="success" @click="send2Jarvis">Senden</v-btn>

  <v-theme-provider theme="dark">
    <v-container fluid class="d-flex flex-lg-row flex-column justify-center" style="max-width: 50%;">
			<v-expansion-panels>
        <v-expansion-panel class="bg-black">
          <v-expansion-panel-title class="bg-black">
            <h3 class="ma-2 font-italic" style="flex: 1">Developer Triggers</h3>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-btn class="ma-2" @click="triggerGuMo">Guten Morgen</v-btn>
            <v-btn class="ma-2" @click="triggerSpSu">Spar Support</v-btn>
            <v-btn class="ma-2" @click="triggerNetflix">Netflix & Chill</v-btn>
          </v-expansion-panel-text>
        </v-expansion-panel>
			</v-expansion-panels>
    </v-container>
  </v-theme-provider>
</template>

<script>
import axios from "axios";
import tts from "@/mixins/tts.js";
import stt from "@/mixins/stt.js";

export default {
  data() {
    return {
      jarvisText: "",
      userText: "",
      speaking: false,
      listening: false,
    };
  },
  mixins: [tts, stt],

  mounted() {
    this.speechRecognition.onresult = this.recognitionResult;
    this.speechRecognition.onend = () => {
      this.listening = false;
    };
  },

	sockets: {
		connect() {
			console.log('socket connected')
		},
		proaktiv(data) {
			console.log('Proaktiv data received', data.text)
			this.setJarvisText(data)
		}
	},

  methods: {
    send2Jarvis(event) {
      axios
        .post("http://127.0.0.1:8000/input", this.userText)
        .then((response) => {
          console.log(
            "Asking Jarvis: " +
              this.userText +
              "; Jarvis response: " +
              response.data
          );
					this.setJarvisText(response.data)
        })
				.catch((error) => {
					console.log(error)
					alert(error)
				})
    },

		setJarvisText(text) {
			var imageUrl = text.image
			var linkUrl = text.link
      this.jarvisText = text.text

      if (linkUrl) {
        this.jarvisText += ` <a href="${linkUrl}" target="_blank">${linkUrl}</a>`;
      }

			this.speaking = true
			this.speakString(text.text, () => {
				console.log("Finished speaking");
				this.speaking = false;
			});
		},

    startStopListening() {
      this.listening = !this.listening;
      if (this.listening) {
        this.speechRecognition.start();
      } else {
        this.speechRecognition.stop();
      }
    },

    recognitionResult(event) {
      var final_transcript = "";
      var interim_transcript = "";

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          final_transcript += event.results[i][0].transcript;
        } else {
          interim_transcript += event.results[i][0].transcript;
        }
      }

      if (final_transcript) {
        this.userText = final_transcript;
        this.send2Jarvis();
      } else {
        this.userText = interim_transcript;
      }

      console.log("Final Transcript:", final_transcript);
      console.log("Interim Transcript:", interim_transcript);
    },

    triggerGuMo() {
			console.log("calling good morning usecase procativ")
			axios.get("http://127.0.0.1:8000/trigger/guten_morgen")
		},

		triggerSpSu() {
			console.log("calling savings support usecase procativ")
			let data = axios.get("http://127.0.0.1:8000/trigger/sparsupport")
      console.log(data)

		},

		triggerNetflix() {
			console.log("calling netflix and chill usecase procativ")
			axios.get("http://127.0.0.1:8000/trigger/netflix")
		},
  },
};
</script>
