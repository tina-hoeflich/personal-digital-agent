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
  <h1>{{ jarvisText }}</h1>
  <v-row align="center"
      justify="center">
    <v-col cols="11">
      <v-textarea clearable label="Eingabe" v-model="userText"></v-textarea>
    </v-col>
    <v-col cols="1">
      <v-btn icon="mdi-microphone" color="primary" size="x-large" :active="listening" @click="startStopListening()"></v-btn>
    </v-col>
  </v-row>
  <v-btn size="large" color="success" @click="send2Jarvis">Senden</v-btn>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      jarvisText: "",
      userText: "",
      speaking: false,
      listening: false
    };
  },
  methods: {
    send2Jarvis(event) {
      axios
        .post("http://127.0.0.1:8000/input", this.userText)
        .then((response) => {
          console.log("Jarvis response", response);
          this.jarvisText = response.data;
        });
    },
    animate() {
      this.speaking = true;
      setTimeout(() => {
        this.speaking = false;
      }, 2000);
    },
    startStopListening() {
      this.listening = !this.listening;
    }
  },
};
</script>
