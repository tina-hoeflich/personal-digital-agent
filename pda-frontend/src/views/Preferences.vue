<template>
  <v-theme-provider theme="dark">
    <v-container fluid class="d-flex flex-lg-row flex-column justify-center">
      <v-card 
        v-for="pane in settings"
        class="ma-2"
        style="flex: 1"
      >
      <v-card-item>
        <v-card-title class="float-left">
          {{ pane.title }}
        </v-card-title>
      </v-card-item>
      <v-card-text class="float-left">
        This is example Text
      </v-card-text>
      </v-card>
    </v-container>
  </v-theme-provider>
</template>
  
<script>
export default {
  data() {
    return {
      settings: [
        { title: "Personal Info"},
        { title: "Navigation Settings"},
        { title: "Important Contacts"},
        { title: "Financials"},
      ],
    };
  },
};
</script>

<style>

</style>