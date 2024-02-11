<script setup>
import { ref } from "vue";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";
import {useUserStore} from "@/stores/useUserStore";

const authStore = useAuthStore();
const doctorStore = useDoctorStore();
const role = useUserStore().user.role;
const isDark = localStorage.getItem("darkTheme") === "true";
const body = document.querySelector("body");

const backgroundImage = "../../background.png";

const doctor = doctorStore.doctor;

const form = ref({
  firstName: doctor.firstName || "",
  lastName: doctor.lastName || "",
  specialty: doctor.specialty || "",
  address: doctor.address || "",
  phoneNumber: doctor.phoneNumber || "",
  dateOfBirth: doctor.dateOfBirth || null,
});

const dateFormat = (date) => {
  return date.toLocaleDateString("hr-HR");
};

const submit = async () => {
  try {
    await doctorStore.updateDoctor(form.value);
    await router.push("/doctor");
  } catch (error) {
    console.log(error);
  }
};

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (role !== "doctor") {
  console.log("Nemate pristup ovoj stranici");
  router.push("/dashboard");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <v-img :src="backgroundImage" cover height="100%">
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
                  Specijalnost
                </div>
                <v-text-field
                  density="compact"
                  placeholder="Unesi specijalnost"
                  variant="outlined"
                  v-model="form.specialty"
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
  </v-img>
</template>

<style scoped>

</style>
