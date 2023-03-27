<template>
  <v-theme-provider theme="dark">
    <v-form v-model="valid" fast-fail @submit.prevent>
      <v-container fluid class="d-flex flex-lg-row flex-column justify-center">
        <v-card class="ma-2" style="flex: 1">

          <v-card-item>
            <v-card-title class="float-left">
              Personal Settings
            </v-card-title>
          </v-card-item>

          <v-card-text>
              <v-text-field
                v-model="settingsJSON.goodMorning.name"
                :rules="basicRules"
                :counter="50"
                label="Name"
                required
              ></v-text-field>
              <v-text-field
                v-model="settingsJSON.goodMorning.homeAddress"
                :rules="basicRules"
                :counter="50"
                label="Home Adress"
                required
              ></v-text-field>
          </v-card-text>

        </v-card>

        <v-card class="ma-2" style="flex: 1">

          <v-card-item>
            <v-card-title class="float-left">
              Navigation Settings
            </v-card-title>
          </v-card-item>

          <v-card-text>
              <v-text-field
                v-model="settingsJSON.goodMorning.workAddress"
                :rules="basicRules"
                :counter="50"
                label="Work Address"
                required
              ></v-text-field>
              <v-select
              label="Mode of Transporation"
              v-model="settingsJSON.goodMorning.modeOfTransportation"
              :items="['Car', 'Bike', 'Walking']"
              :rules="[v => !!v || 'Item is required']"
              >
              </v-select>
              <v-select
              label="Fuel Type"
              v-model="settingsJSON.sparen.sprit.typ"
              :items="['e5', 'e10', 'diesel']"
              :rules="[v => !!v || 'Item is required']"
              >
              </v-select>
          </v-card-text>

        </v-card>

        <v-card class="ma-2" style="flex: 1">

          <v-card-item>
            <v-card-title class="float-left">
              Important Contacts
            </v-card-title>
          </v-card-item>

          <v-card-text>
              <v-text-field
                v-model="settingsJSON.depressionHandler.emergencyEmail"
                :rules="emailRules"
                :counter="50"
                label="Emergency Email"
                required
              ></v-text-field>
              <v-text-field
                v-model="settingsJSON.depressionHandler.friendEmail"
                :rules="emailRules"
                :counter="50"
                label="Personal Friend Email"
                required
              ></v-text-field>
          </v-card-text>

        </v-card>

      </v-container>
			<v-divider></v-divider>
			<h2>Favorite Stocks</h2>
      <v-container fluid class="d-flex flex-lg-row flex-column justify-center">
        <v-card class="ma-2" style="flex: 1" v-for="(stock, index) in settingsJSON.sparen.stocks.favorites">

          <v-card-item>
            <v-card-title class="float-left">
              {{stock.symbol != "" ? stock.symbol : "--" }}
            </v-card-title>
          </v-card-item>

          <v-card-text>
              <v-text-field
              v-model="stock.symbol"
              :rules="stockRules"
              :counter="12"
              label="Stock Symbol"
              required
            ></v-text-field>
            <v-text-field
              v-model="stock.priceHigh"
              :rules="numberRules"
              :counter="12"
              label="Maximum Price"
              required
            ></v-text-field>
            <v-text-field
              v-model="stock.priceLow"
              :rules="numberRules"
              :counter="12"
              label="Minimum Price"
              required
            ></v-text-field>
          </v-card-text>

					<v-card-actions>
      			<v-btn
        			variant="text"
        			color="red-lighten-1"
							@click="settingsJSON.sparen.stocks.favorites.splice(index, 1)"
      			>
						Remove
      			</v-btn>
    			</v-card-actions>

        </v-card>
      </v-container>
			<v-btn
				prepend-icon="mdi-plus"
				@click="settingsJSON.sparen.stocks.favorites.push({symbol: '', priceHigh: '', priceLow: ''})"
			> Add Stock
			</v-btn>
			<v-divider></v-divider>
      <v-btn type="submit" size="large" color="success" class="mt-2" @click="submit">Submit settings</v-btn>
    </v-form>
  </v-theme-provider>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      valid: false,

      // Input rules
      basicRules: [
        value => {
          if (value) return true

          return '*Required'
        },
        value => {
          if (value?.length <= 50) return true

          return 'Input must be less than 50 characters.'
        },
      ],
      emailRules: [
        value => {
          if (value) return true

          return 'E-mail is required.'
        },
        value => {
          if (/.+@.+\..+/.test(value)) return true

          return 'E-mail must be valid.'
        },
      ],
      stockRules: [
      value => {
          if (value) return true

          return 'Stock Symbol is required.'
        },
        value => {
          if (/^[A-Z]+/.test(value)) return true

          return 'Input must start with Capital letter'
        },
        value => {
          if (/^[A-Z0-9\.\:]+$/.test(value)) return true

          return 'Input may only contain Capital letters and Numbers'
        },
      ],
      numberRules: [
      value => {
          if (value) return true

          return 'Number is required.'
        },
        value => {
          if (/^[0-9]+$/.test(value)) return true

          return 'You can only input numbers!'
        },
      ],

      // JSON Document Variable
      settingsJSON: {
        "example": {
          "name": "How to use settings.json"
        },
        "goodMorning": {
          "name": '',
          "homeAddress": '',
          "workAddress": '',
          "modeOfTransportation": '',
        },
        "depressionHandler": {
          "emergencyEmail": '',
          "friendEmail": '',
        },
        "sparen": {
          "sprit": {
            "typ": '',
            "lat": 48.83421132375812,
            "lng":  9.152560823835184,
            "radius": 5,
            "preisschwelle": 1.299
          },
          "stocks": {
            "favorites": [
              {
                "symbol": '',
                "priceHigh": '',
                "priceLow": ''
              },
            ]
          }
        }
      },
    };
  },
  methods: {
    async submit () {
      if(this.valid) {
        console.log("sumbitting settings...", JSON.stringify(this.settingsJSON))
        axios.post("http://127.0.0.1:8000/settings", this.settingsJSON)
        .then((response) => {
          console.log(response)
        })
      }
      else {
        console.log("Error: Input fields not properly filled in")
      }
    },
    async getPreferences () {
      console.log("getting settings... ")
      axios.get("http://127.0.0.1:8000/settings")
        .then((response) => {
          console.log(response)
          this.settingsJSON = response.data
        })
    }
  },
  mounted: function() {
    this.getPreferences()
  }
};
</script>

<style>

</style>
