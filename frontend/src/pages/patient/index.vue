<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const authStore = useAuthStore();
const userStore = useUserStore();
const patientStore = usePatientStore();
const role = userStore.user.role;

const backgroundImage = "../../background.png";

const patient = patientStore.patient;
const patientDateOfBirth = new Date(patient.dateOfBirth).toLocaleDateString("hr-HR");

const title = "Moji podaci";
const patientData = [
  {
    title: "Ime",
    value: `${patient.firstName}`,
  },
  {
    title: "Prezime",
    value: `${patient.lastName}`,
  },
  {
    title: "Adresa",
    value: `${patient.address}`,
  },
  {
    title: "Broj telefona",
    value: `${patient.phoneNumber}`,
  },
  {
    title: "Datum rođenja",
    value: `${patientDateOfBirth}`,
  },
];

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
} else if (!authStore.auth.hasProfile) {
  router.push("/patient/create");
} else if (role !== 'patient') {
  router.push("/dashboard");
}

</script>

<template>
  <v-img :src="backgroundImage" cover height="100%">
    <v-btn
        @click="router.go(-1)"
        size="large"
        class="mt-6 mx-6">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5">{{ title }}</v-card-title>
          <v-card-item>
            <v-sheet>
              <v-card-text
                v-for="item in patientData"
                :key="item"
                class="v-card-text"
              >
                <div class="text-subtitle-1 text-medium-emphasis">
                  {{ item.title }}
                </div>
                <v-text-field
                  disabled
                  readonly
                  density="compact"
                  variant="outlined"
                  >{{ item.value }}</v-text-field
                >
              </v-card-text>
              <v-btn
                border
                block
                size="large"
                class="mb-8 mt-6"
                color="blue-darken-2"
                variant="tonal"
                append-icon="mdi-pencil"
                :to="`/patient/update`"
                >Uredi</v-btn
              >
            </v-sheet>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </v-img>
</template>

<style scoped>
.v-card-text {
  padding: 0 !important;
}

</style>
