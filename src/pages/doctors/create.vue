<script setup>
import { ref } from "vue";
import { usePatientStore } from "@/stores/usePatientStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const form = ref({
  firstName: "",
  lastName: "",
  address: "",
  phoneNumber: "",
  dateOfBirth: null,
});

const firstNameRule = [
  (v) => !!v || "Ime je obavezno",
  (v) => (v && v.length <= 20) || "Ime mora biti manje od 20 karaktera",
];

const lastNameRule = [
  (v) => !!v || "Prezime je obavezno",
  (v) => (v && v.length <= 20) || "Prezime mora biti manje od 20 karaktera",
];

const phoneNumberRule = [
  (v) => {
    const numberWithoutSpace = v.replace(/\s+/g, "");

    const regex = /^[0-9+]+$/;
    if (!regex.test(numberWithoutSpace) && numberWithoutSpace !== "") {
      return "Broj telefona nije validan. Dozvoljeni su samo brojevi i znak +";
    }
    return true;
  },
];

const userStore = useUserStore();
const authStore = useAuthStore();
const role = userStore.user.role;

const submit = async () => {
  if (role === "patient") {
    try {
      const patientStore = usePatientStore();
      await patientStore.createPatient(form.value);
    } catch (error) {
      console.log(error);
    }
  } else if (role === "doctor") {
    try {
      const doctorStore = useDoctorStore();
      await doctorStore.createDoctor(form.value);
    } catch (error) {
      console.log(error);
    }
  }
};

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (authStore.auth.hasProfile) {
  router.push("/profile");
}
</script>

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
                  v-model="form.firstName"
                  :rules="firstNameRule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Prezime</div>
                <v-text-field
                  density="compact"
                  placeholder="Unesi prezime"
                  variant="outlined"
                  v-model="form.lastName"
                  :rules="lastNameRule"
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
                  v-model="form.phoneNumber"
                  :rules="phoneNumberRule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Datum rođenja
                </div>
                <v-container>
                  <v-row justify="center">
                    <v-locale-provider locale="hr">
                      <v-date-picker
                        width="100%"
                        v-model="form.dateOfBirth"
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
                  >Spremi</v-btn>
              </v-form>
            </v-sheet>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
