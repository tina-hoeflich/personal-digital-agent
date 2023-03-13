<template>
  <v-img contain src="@/assets/jarvis.png" max-height="300px" />
  <h1>{{ jarvisText }}</h1>
  <v-textarea clearable label="Eingabe" v-model="userText"></v-textarea>
  <v-btn size="large" color="success" @click="send2Jarvis">Senden</v-btn>
</template>

<script>
export default {
  data() {
    return {
      jarvisText: "",
      userText: "",
    };
  },
  methods: {
    send2Jarvis(event) {
      alert(`Hello ${this.userText}!`);
    },
  },
};
</script>
