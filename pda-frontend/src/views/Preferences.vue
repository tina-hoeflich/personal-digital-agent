<template>
  <v-theme-provider theme="dark">
    <v-form v-model="valid" @submit.prevent>
      <v-container fluid class="d-flex flex-lg-row flex-column justify-center">
        <v-card class="ma-2" style="flex: 1">

          <v-card-item>
            <v-card-title class="float-left">
              Personal Settings
            </v-card-title>
          </v-card-item>

          <v-card-text>
              <v-text-field
                v-model="name"
                :rules="basicRules"
                :counter="50"
                label="Name"
                required
              ></v-text-field>
              <v-text-field
                v-model="homeAddress"
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
                v-model="workAddress"
                :rules="basicRules"
                :counter="50"
                label="Work Address"
                required
              ></v-text-field>
              <v-select
              label="Mode of Transporation"
              v-model="modeOfTP"
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
                v-model="emergencyEmail"
                :rules="emailRules"
                :counter="50"
                label="Emergency Email"
                required
              ></v-text-field>
              <v-text-field
                v-model="friendEmail"
                :rules="emailRules"
                :counter="50"
                label="Personal Friend Email"
                required
              ></v-text-field>
          </v-card-text>

        </v-card>

        <v-card class="ma-2" style="flex: 1">

          <v-card-item>
            <v-card-title class="float-left">
              Financial Settings
            </v-card-title>
          </v-card-item>

          <v-card-text>
              <v-text-field
                v-model="stockSymbol
                "
                :rules="stockRules"
                :counter="12"
                label="Security ISIN"
                required
              ></v-text-field>
              <v-select
              label="Fuel Type"
              v-model="fuelType"
              :items="['Diesel', 'Gasoline']"
              :rules="[v => !!v || 'Item is required']"
              >
              </v-select>
          </v-card-text>

        </v-card>
      </v-container>
      <v-btn type="submit" size="large" color="success" class="mt-2" @click="submit">Submit</v-btn>
    </v-form>
  </v-theme-provider>
</template>
  
<script>
import axios from "axios";
export default {
  data() {
    return {
      valid: false,

      // Text field input variables 
      name: '',
      homeAddress: '',
      workAddress: '',
      emergencyEmail: '',
      friendEmail: '',
      stockSymbol: '',

      // Selector input variables
      modeOfTP: '',
      fuelType: '',

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

          return 'Number is required.'
        },
        value => {
          if (/^[A-Z]+\:[A-Z]+/.test(value)) return true

          return 'Input must be of shape XXX:XXX'
        },
      ],

      // JSON Document Variable
      settingsJSON: {},
    };
  },
  methods: {
    async submit () {
      if(this.valid) {
        // Create JSON Doc
        this.settingsJSON = {
          "goodMorning": {
            "name": this.name,
            "homeAddress": this.homeAddress,
            "workAddress": this.workAddress,
            "modeOfTransportation": this.modeOfTP,
          },
          "depressionHandler": {
            "emergencyEmail": this.emergencyEmail,
            "friendEmail": this.friendEmail,
          },
          "savingSupport": {
            "stockSymbol": this.stockSymbol,
            "fueTtype": this.fuelType
          }
        }
        console.log("sumbitting settings...", JSON.stringify(this.settingsJSON))
        axios.post("http://127.0.0.1:8000/setPreferences", this.settingsJSON)
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
      axios.get("http://127.0.0.1:8000/getPreferences")
        .then((response) => {
          console.log(response)
          let userSettings = response.data
          this.name = userSettings.goodMorning.name
          this.homeAddress = userSettings.goodMorning.homeAddress
          this.workAddress = userSettings.goodMorning.workAddress
          this.modeOfTP = userSettings.goodMorning.modeOfTransportation
          this.emergencyEmail = userSettings.depressionHandler.emergencyEmail
          this.friendEmail = userSettings.depressionHandler.friendEmail
          this.stockSymbol = userSettings.savingSupport.stockSymbol
          this.fuelType = userSettings.savingSupport.fuelType
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