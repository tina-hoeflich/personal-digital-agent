<template>
  <div @click="animate()" style="height: 400px">
    <v-img v-if="speaking" contain src="@/assets/circles_spinning.gif" max-height="400px" />
    <v-img v-else contain src="@/assets/frame_0.png" max-height="400px" />
  </div>
  <h1>{{ jarvisText }}</h1>
  <v-textarea clearable label="Eingabe" v-model="userText"></v-textarea>
  <v-btn size="large" color="success" @click="send2Jarvis">Senden</v-btn>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      jarvisText: "",
      userText: "",
      speaking: false
    };
  },
  methods: {
    send2Jarvis(event) {
      axios.post("http://127.0.0.1:8000/input", this.userText)
      .then((response) => {
        console.log("Jarvis response", response)
        this.jarvisText = response.data
      })
    },
    animate() {
      this.speaking = true;
      setTimeout(() => {
        this.speaking = false;
      }, 2000)
    }
  },
};
</script>