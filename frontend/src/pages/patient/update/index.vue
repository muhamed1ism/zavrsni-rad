<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { useUserStore } from "@/stores/useUserStore";
import { usePatientStore } from "@/stores/usePatientStore";
import router from "@/router";

const authStore = useAuthStore();
const patientStore = usePatientStore();
const role = useUserStore().user.role;
const isDark = localStorage.getItem("darkTheme") === "true";
const body = document.querySelector("body");

const patient = patientStore.patient;

const form = ref({
  firstName: patient.firstName || "",
  lastName: patient.lastName || "",
  address: patient.address || "",
  phoneNumber: patient.phoneNumber || "",
  dateOfBirth: patient.dateOfBirth || null,
});

const dateFormat = (date) => {
  return date.toLocaleDateString("hr-HR");
};

const convertToISO = (date) => {
  return new Date(date).toISOString();
};

const submit = async () => {
  try {
    form.value.dateOfBirth = convertToISO(form.value.dateOfBirth);
    const patientStore = usePatientStore();
    await patientStore.updatePatient(form.value);
    await router.push("/patient");
  } catch (error) {
    console.log(error);
  }
};

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (role !== "patient") {
  console.log("Nemate pristup ovoj stranici");
  router.push("/dashboard");
}

if (!authStore.auth.hasProfile) {
  router.push("/patient/create");
}
</script>

<template>
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5">Moji podaci</v-card-title>
          <v-card-item>
            <v-sheet>
              <v-form @submit.prevent="submit">
                <div class="text-subtitle-1 text-medium-emphasis">Ime</div>
                <v-text-field
                  density="compact"
                  placeholder="Unesi ime"
                  variant="outlined"
                  v-model="form.firstName"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Prezime</div>
                <v-text-field
                  density="compact"
                  placeholder="Unesi prezime"
                  variant="outlined"
                  v-model="form.lastName"
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
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Datum rođenja
                </div>
                <v-container>
                  <v-row justify="center">
                    <VueDatePicker
                      v-model="form.dateOfBirth"
                      placeholder="Unesi datum rođenja"
                      :format="dateFormat"
                      locale="hr"
                      auto-apply
                      :enable-time-picker="false"
                      :teleport="body"
                      :dark="isDark"
                    ></VueDatePicker>
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
                  block
                  variant="tonal"
                  color="blue-darken-2"
                  size="large"
                  class="mb-8 mt-2"
                  @click="submit"
                  >Ažuriraj</v-btn
                >
              </v-form>
            </v-sheet>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
