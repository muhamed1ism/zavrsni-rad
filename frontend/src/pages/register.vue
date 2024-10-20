<script setup>
import router from "@/router";
import { ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { useUserStore } from "@/stores/useUserStore";
import { rules } from "@/components/FormValidationRules.vue";
import BackButton from "@/components/BackButton.vue";
import Background from "@/components/Background.vue";

const form = ref({
  email: "",
  password: "",
  passwordConfirm: "",
  role: "patient",
});
const alertVisible = ref(false);
const alertMessage = ref("");
const visible = ref(false);

const userStore = useUserStore();
const authStore = useAuthStore();

const submit = async () => {
  try {
    await authStore.register(form.value);
    await userStore.getUser();
    await router.push("/dashboard");
  } catch (error) {
    console.log(error);
    if (error.response.status === 409) {
      alertMessage.value = (
          "User with this email already exists" +
          " or passwords do not match"
      );
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
            <v-card-title class="text-center text-h5"
              >Register</v-card-title
            >
            <v-card-item>
              <v-sheet>
                <v-form @submit.prevent="submit">
                  <v-label
                    class="text-subtitle-1 text-hard-emphasis"
                    text="Email"
                  />
                  <v-text-field
                    density="compact"
                    placeholder="Enter email address"
                    variant="outlined"
                    v-model="form.email"
                    :rules="rules.email"
                  ></v-text-field>

                  <v-label
                    class="text-subtitle-1 text-hard-emphasis"
                    text="Password"
                  />
                  <v-text-field
                    :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'"
                    density="compact"
                    placeholder="Enter password"
                    variant="outlined"
                    v-model="form.password"
                    @click:append-inner="visible = !visible"
                    :rules="rules.password"
                  ></v-text-field>

                  <v-label
                    class="text-subtitle-1 text-hard-emphasis"
                    text="Confirm password"
                  />
                  <v-text-field
                    :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'"
                    density="compact"
                    placeholder="Enter password again"
                    variant="outlined"
                    v-model="form.passwordConfirm"
                    @click:append-inner="visible = !visible"
                    :rules="rules.passwordConfirm(form.password)"
                  ></v-text-field>

                  <div
                    class="mt-6 text-center text-subtitle-1 text-medium-emphasis"
                  >
                    Are you a patient or a doctor?
                  </div>
                  <v-container
                    class="d-flex justify-center align-content-center"
                  >
                    <v-radio-group v-model="form.role" inline :rules="rules.role">
                      <v-container class="d-flex justify-space-evenly">
                        <v-radio
                          label="Patient"
                          color="blue"
                          value="patient"
                        ></v-radio>
                        <v-radio
                          label="Doctor"
                          color="red"
                          value="doctor"
                        ></v-radio>
                      </v-container>
                    </v-radio-group>
                  </v-container>

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
                    class="my-2"
                    >Register</v-btn
                  >
                  <v-card-text class="text-center text-medium-emphasis pb-6">Have an account? <RouterLink to="/login" class="text-blue-darken-2 text-decoration-none">Login</RouterLink></v-card-text>
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
