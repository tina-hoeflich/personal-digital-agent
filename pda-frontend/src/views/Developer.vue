<template>
  <v-theme-provider theme="dark">
    <v-container fluid class="d-flex flex-lg-row flex-column justify-center">
      <v-card class="ma-2" style="flex: 1">

        <v-card-item>
          <v-btn size="large" color="success" class="ma-2" @click="callGoodMorning">Good Morning</v-btn>
        </v-card-item>

        <v-card-text>
          <v-textarea
            v-model="goodMorningResponse"
            append-inner-icon="mdi-comment"
            auto-grow
            clearable
            persistent-clear
            clear-icon="mdi-close-circle"
            class="mx-2"
            rows="5"
          ></v-textarea>
        </v-card-text>

      </v-card>

      <v-card class="ma-2" style="flex: 1">

        <v-card-item>
          <v-btn size="large" color="success" class="ma-2" @click="callDepressionHandler">Depression Handler</v-btn>
        </v-card-item>

        <v-card-text>
          <v-textarea
            v-model="depressionHandlerResponse"
            append-inner-icon="mdi-comment"
            auto-grow
            clearable
            persistent-clear
            clear-icon="mdi-close-circle"
            class="mx-2"
            rows="5"
          ></v-textarea>
        </v-card-text>

      </v-card>

      </v-container>
      <v-container fluid class="d-flex flex-lg-row flex-column justify-center">

      <v-card class="ma-2" style="flex: 1">

        <v-card-item>
          <v-btn size="large" color="success" class="ma-2" @click="callSavingsSupport('fuel')">Savings Support - Fuel</v-btn>
          <v-btn size="large" color="success" class="ma-2" @click="callSavingsSupport('stock')">Savings Support - Stocks</v-btn>
        </v-card-item>

        <v-card-text>
          <v-textarea
            v-model="savingsSupportResponse"
            append-inner-icon="mdi-comment"
            auto-grow
            clearable
            persistent-clear
            clear-icon="mdi-close-circle"
            class="mx-2"
            rows="5"
          ></v-textarea>
        </v-card-text>

      </v-card>

    <v-card class="ma-2" style="flex: 1">

      <v-card-item>
        <v-btn size="large" color="success" class="ma-2" @click="callNetflixAndChill">Netflix And Chill</v-btn>
      </v-card-item>

      <v-card-text>
        <v-textarea
            v-model="netflixAndChillResposne"
            append-inner-icon="mdi-comment"
            auto-grow
            clearable
            persistent-clear
            clear-icon="mdi-close-circle"
            class="mx-2"
            rows="5"
          ></v-textarea>
      </v-card-text>

    </v-card>
    </v-container>
  </v-theme-provider>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      goodMorningResponse: '',
      depressionHandlerResponse: '',
      savingsSupportResponse: '',
      netflixAndChillResposne: ''
    }
  },
  methods: {
    callGoodMorning() {
      this.goodMorningResponse = "Good Morning!"
    },
    callDepressionHandler() {
      this.depressionHandlerResponse = "Y U sad? :("
    },
    callSavingsSupport(type) {
      let input = "save " + type
      console.log("calling savings support with input", input)
      axios.post("http://127.0.0.1:8000/input", input)
      .then((response) => {
        console.log(response)
        this.savingsSupportResponse = response.data
      })
      
    },
    callNetflixAndChill() {
      this.netflixAndChillResposne = "U up? ^^"
    }
  }
}
</script>
  