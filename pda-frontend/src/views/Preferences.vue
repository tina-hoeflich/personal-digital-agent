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
                label="Name"
                required
              ></v-text-field>
              <v-text-field
                v-model="settingsJSON.goodMorning.homeAddress"
                :rules="basicRules"
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
                label="Emergency Email"
                required
              ></v-text-field>
              <v-text-field
                v-model="settingsJSON.depressionHandler.friendEmail"
                :rules="emailRules"
                label="Personal Friend Email"
                required
              ></v-text-field>
          </v-card-text>

        </v-card>

      <v-card class="ma-2" style="flex: 1">

        <v-card-item>
          <v-card-title class="float-left">
            Fuel Settings
          </v-card-title>
        </v-card-item>

        <v-card-text>
          <v-select
              label="Fuel Type"
              v-model="settingsJSON.sparen.sprit.typ"
              :items="['e5', 'e10', 'diesel']"
              :rules="[v => !!v || 'Item is required']"
              >
            </v-select>
            <v-text-field
              v-model.number="settingsJSON.sparen.sprit.radius"
              :rules="numberRules"
              label="Gas station radius (km)"
              required
            ></v-text-field>
            <v-text-field
              v-model.number="settingsJSON.sparen.sprit.preisschwelle"
              :rules="numberRules"
              append-inner-icon="mdi-currency-eur"
              label="Price threshold"
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
              label="Stock Symbol"
              required
            ></v-text-field>
            <v-text-field
              v-model.number="stock.priceHigh"
              :rules="numberRules"
              label="Maximum Price"
              required
            ></v-text-field>
            <v-text-field
              v-model.number="stock.priceLow"
              :rules="numberRules"
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
      <v-btn 
        type="submit" 
        size="large" 
        color="success" 
        class="mt-2" 
        @click="submit"
      >
      Submit settings</v-btn>
      <v-scroll-x-transition>
        <v-icon
          v-if="submitted"
          class="ma-2 pa-2 pt-4"
          color="success"
        >
        mdi-check-circle-outline
        </v-icon>
    </v-scroll-x-transition>
    </v-form>
  </v-theme-provider>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      valid: false,

      submitted: false,

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
          if (/^[0-9]+(\.[0-9]+)?$/.test(value)) return true

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
            "radius": 0,
            "preisschwelle": 0,
          },
          "stocks": {
            "favorites": [
              {
                "symbol": '',
                "priceHigh": 0,
                "priceLow": 0
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
          console.log(response);
          this.submitted = true;
          setTimeout(() => {
            this.submitted = false;
          }, 1000)
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
