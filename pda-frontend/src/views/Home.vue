<template>
  <v-img contain src="@/assets/jarvis.png" max-height="300px" />
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
  },
};
</script>
