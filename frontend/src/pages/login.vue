<script setup>
import router from "@/router";
import { ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useUserStore } from "@/stores/useUserStore";
import { rules } from "@/components/FormValidationRules.vue";
import BackButton from "@/components/BackButton.vue";
import Background from "@/components/Background.vue";

const form = ref({
  email: "",
  password: "",
});
const alertVisible = ref(false);
const alertMessage = ref("");
const visible = ref(false);

const userStore = useUserStore();
const authStore = useAuthStore();
const doctorStore = useDoctorStore();
const patientStore = usePatientStore();

const submit = async () => {
  try {
    await authStore.login(form.value);
    await userStore.getUser();
    if (userStore.user.role === "patient") await patientStore.getPatient();
    else if (userStore.user.role === "doctor") await doctorStore.getDoctor();
    await router.push("/dashboard");
    window.location.reload();
  } catch (error) {
    console.log(error);
    if (error.response.status === 401) {
      alertMessage.value = "Wrong email or password";
      alertVisible.value = true;
    }
  }
};

if (authStore.auth.isAuthenticated) router.push("/dashboard");
</script>

<template>
  <Background>
    <BackButton position="absolute" />
    <v-container fluid class="fill-height">
      <v-row class="justify-center mb-16">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card border variant="flat" class="pa-4 my-12">
            <v-card-title class="text-center text-h5">Login</v-card-title>
            <v-card-item>
              <v-sheet>
                <v-form @submit.prevent="submit">
                  <v-label
                    class="text-subtitle-1 text-hard-emphasis"
                    text="Email"
                  />

                  <v-text-field
                    density="compact"
                    placeholder="Email address"
                    prepend-inner-icon="mdi-email-outline"
                    variant="outlined"
                    v-model="form.email"
                    :rules="rules.email"
                  ></v-text-field>

                  <div
                    class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
                  >
                    Password
                  </div>

                  <v-text-field
                    :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'"
                    density="compact"
                    placeholder="Enter password"
                    prepend-inner-icon="mdi-lock-outline"
                    variant="outlined"
                    v-model="form.password"
                    @click:append-inner="visible = !visible"
                    :rules="rules.password"
                  ></v-text-field>

                  <v-alert
                    v-model="alertVisible"
                    density="compact"
                    variant="tonal"
                    type="error"
                  >
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
                    >Login</v-btn
                  >

                  <v-card-text class="text-center">
                    <RouterLink
                      class="text-blue-darken-2 text-decoration-none"
                      to="/register"
                    >
                      Create an account <v-icon icon="mdi-chevron-right" />
                    </RouterLink>
                  </v-card-text>
                </v-form>
              </v-sheet>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </Background>
</template>

<style scoped></style>
