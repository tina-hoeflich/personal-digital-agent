<template>
  <div id="app2">
    <v-app>
      <v-app-bar app color="primary" fixed>
        <v-app-bar-title class="mr-4 white--text">
          J.A.R.V.I.S.
        </v-app-bar-title>
        <v-toolbar-items>
          <v-btn
            v-for="item in navItems"
            :key="item.title"
            :to="item.link"
            class="align-center"
            color="white"
          >
            <v-icon class="mr-2">{{ item.icon }}</v-icon>
            {{ item.title }}
          </v-btn>
        </v-toolbar-items>
        <v-spacer />

        <v-btn
          icon
          target="_blank"
          href="https://github.com/tina-hoeflich/personal-digital-agent"
        >
          <v-icon color="white">mdi-github</v-icon>
        </v-btn>
      </v-app-bar>

      <!-- Hauptbereich der Website -->
      <v-main>
        <v-container fluid>
          <!-- Der Router view lädt alle Seiten rein -->
          <router-view></router-view>
        </v-container>
      </v-main>
    </v-app>
  </div>
</template>

<script>
export default {
  data() {
    return {
      navItems: [
        { title: "Assistant", icon: "mdi-google-assistant", link: "/" },
        { title: "Developer", icon: "mdi-laptop", link: "/developer" },
      ],
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

}
</style>
