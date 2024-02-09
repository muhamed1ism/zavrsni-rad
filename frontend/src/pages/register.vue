<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";
import { useUserStore } from "@/stores/useUserStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useDoctorStore } from "@/stores/useDoctorStore";

const form = ref({
  email: "",
  password: "",
  passwordConfirm: "",
  role: "patient",
});

const alertVisible = ref(false);
const alertMessage = ref("");
const visible = ref(false);

const backgroundImage = "../../background.png";

const emailRule = [
  (v) => !!v || "Email je obavezan",
  (v) => /.+@.+/.test(v) || "Email nije validan",
];

const passwordRule = [
  (v) => !!v || "Lozinka je obavezna",
  (v) => (v && v.length >= 8) || "Lozinka mora biti duža od 8 karaktera",
];

const passwordConfirmRule = [
  (v) => !!v || "Potvrda lozinke je obavezna",
  (v) => v === form.value.password || "Lozinke se ne poklapaju",
];

const roleRule = [(v) => !!v || "Role je obavezan"];

const authStore = useAuthStore();

const submit = async () => {
  try {
    await authStore.register(form.value);
    await useUserStore().getUser();
    const role = useUserStore().user.role;
    if (role === "patient") {
      await usePatientStore().getPatient();
    } else if (role === "doctor") {
      await useDoctorStore().getDoctor();
    }
    await router.push("/dashboard");
  } catch (error) {
    console.log(error);
    if (error.response.status === 409) {
      alertMessage.value = (
          "Korisnik sa ovom email adresom već postoji " +
          "ili niste unijeli ispravno podatke"
      );
      alertVisible.value = true;
    }
  }
};

if (authStore.auth.isAuthenticated) {
  router.push("/dashboard");
}
</script>

<template>
  <v-img :src="backgroundImage" cover height="100%" class="gray-filter">
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5"
            >Registracija računa</v-card-title
          >
          <v-card-item>
            <v-sheet>
              <v-form @submit.prevent="submit">
                <div class="text-subtitle-1 text-medium-emphasis">Email</div>
                <v-text-field
                  density="compact"
                  placeholder="Email adresa"
                  variant="outlined"
                  v-model="form.email"
                  :rules="emailRule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Lozinka</div>
                <v-text-field
                  :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                  :type="visible ? 'text' : 'password'"
                  density="compact"
                  placeholder="Unesite lozinku"
                  variant="outlined"
                  v-model="form.password"
                  @click:append-inner="visible = !visible"
                  :rules="passwordRule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Potvrdi lozinku
                </div>
                <v-text-field
                  :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                  :type="visible ? 'text' : 'password'"
                  density="compact"
                  placeholder="Potvrdi lozinku"
                  variant="outlined"
                  v-model="form.passwordConfirm"
                  @click:append-inner="visible = !visible"
                  :rules="passwordConfirmRule"
                ></v-text-field>

                <div
                  class="mt-6 text-center text-subtitle-1 text-medium-emphasis"
                >
                  Da li si pacijent ili doktor?
                </div>
                <v-container class="d-flex justify-center align-content-center">
                  <v-radio-group v-model="form.role" inline :rules="roleRule">
                    <v-container class="d-flex justify-space-evenly">
                      <v-radio
                        label="Pacijent"
                        color="blue"
                        value="patient"
                      ></v-radio>
                      <v-radio
                        label="Doktor"
                        color="red"
                        value="doctor"
                      ></v-radio>
                    </v-container>
                  </v-radio-group>
                </v-container>

                <v-alert
                  v-if="alertVisible"
                  v-model="alertVisible"
                  density="compact"
                  type="error">
                  {{ alertMessage }}
                </v-alert>

                <v-btn
                  border
                  type="submit"
                  block
                  variant="tonal"
                  color="blue-darken-2"
                  size="large"
                  class="mb-8 mt-2"
                  >Registriraj se</v-btn>
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
.gray-filter {
  background-color: rgba(18, 18, 18, 0.1) !important;
}
</style>
