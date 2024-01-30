<template>
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5"
          >Unesi svoje podatke</v-card-title
          >
          <v-card-item>
            <v-sheet>
              <v-form @submit.prevent="submit">
                <div class="text-subtitle-1 text-medium-emphasis">Ime</div>
                <v-text-field
                    density="compact"
                    placeholder="Unesi ime"
                    variant="outlined"
                    v-model="form.first_name"
                    :rules="first_name_rule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Prezime</div>
                <v-text-field
                    density="compact"
                    placeholder="Unesi prezime"
                    variant="outlined"
                    v-model="form.last_name"
                    :rules="last_name_rule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Adresa stanovanja
                </div>
                <v-text-field
                    density="compact"
                    placeholder="Unesi adresu stanovanja"
                    variant="outlined"
                    v-model="form.address"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Broj telefona
                </div>
                <v-text-field
                    density="compact"
                    placeholder="Unesi broj telefona"
                    variant="outlined"
                    v-model="form.phone_number"
                    :rules="phone_number_rule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Datum rođenja
                </div>
                <v-container>
                  <v-row justify="center">
                    <v-locale-provider locale="hr">
                      <v-date-picker
                          width="100%"
                          v-model="form.date_of_birth"
                          title=""
                          header="Unesi datum"
                          border
                      >
                      </v-date-picker>
                    </v-locale-provider>
                  </v-row>
                </v-container>

                <div class="v-input__details">
                  <div
                      class="v-messages"
                      role="alert"
                      aria-live="polite"
                      id="input-49-messages"
                  ></div>
                  <!---->
                </div>

                <v-btn
                    border
                    type="submit"
                    block
                    variant="tonal"
                    color="blue-darken-2"
                    size="large"
                    class="mb-8 mt-2"
                >Registriraj se</v-btn
                >
              </v-form>
            </v-sheet>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import router from "@/router";
import {usePatientStore} from "@/stores/usePatientStore";

const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  password_confirmation: "",
  address: "",
  phone_number: "",
  date_of_birth: null,
});

const visible = ref(false);

const first_name_rule = [
  (v) => !!v || "Ime je obavezno",
  (v) => (v && v.length <= 20) || "Ime mora biti manje od 20 karaktera",
];

const last_name_rule = [
  (v) => !!v || "Prezime je obavezno",
  (v) => (v && v.length <= 20) || "Prezime mora biti manje od 20 karaktera",
];

const phone_number_rule = [
  (v) => {
    const regex = /^[0-9+]+$/;
    if (!regex.test(v) && v !== "") {
      return "Broj telefona nije validan. Dozvoljeni su samo brojevi i znak +";
    }
    return true;
  },
];

const formatDate = (date_of_birth) => {
  if (!date_of_birth) return null;
  date_of_birth = date_of_birth.toISOString().slice(0, 10);
  const [year, month, day] = date_of_birth.split("-");
  return `${day}.${month}.${year}.`;
};

const patientStore = usePatientStore();

const submit = async () => {
  form.value.date_of_birth = formatDate(form.value.date_of_birth);
  await patientStore.create();
};
</script>
