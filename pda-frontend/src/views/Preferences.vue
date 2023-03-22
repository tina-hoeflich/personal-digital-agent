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
                v-model="stockISIN"
                :rules="isinRules"
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
export default {
  data() {
    return {
      // Text input rules
      valid: false,
      homeAddress: '',
      workAddress: '',
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
      emergencyEmail: '',
      friendEmail: '',
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
      stockISIN: '',
      isinRules: [
      value => {
          if (value) return true

          return 'Number is required.'
        },
        value => {
          if (value?.length != 12 &/^[a-zA-Z][a-zA-Z][0-9-]+/.test(value)) return true

          return 'Input must be of shape XX0000000000'
        },
      ],

      // Selector input variables
      modeOfTP: '',
      fuelType: '',
    };
  },
  methods: {
    async submit () {
      console.log("sumbitting data...")
    },
  }
};
</script>

<style>

</style>