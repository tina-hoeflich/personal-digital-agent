<template>
  <div>
    <audio ref="audio" controls>
      <source :src="songUrl" type="audio/mp3">
    </audio>
    <button v-if="!isPlaying" @click="play">Play</button>
    <button v-else @click="pause">Pause</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      songUrl: "",
      isPlaying: false
    };
  },
  methods: {
    play() {
      this.$refs.audio.play();
      this.isPlaying = true;
    },
    pause() {
      this.$refs.audio.pause();
      this.isPlaying = false;
    }
  },
  mounted() {
    // get the song URL from the backend
    fetch("/get_song")
      .then(response => response.json())
      .then(data => {
        this.songUrl = data.song_url;
      });
  }
};
</script>