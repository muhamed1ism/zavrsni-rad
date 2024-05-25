<script setup>
import router from "@/router";
import { ref } from "vue";
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import { rules } from "@/components/FormValidationRules.vue";
import BackButton from "@/components/BackButton.vue";
import Background from "@/components/Background.vue";

const { auth } = useAuthStore();
const { updatePassword } = useUserStore();

const form = ref({
  currentPassword: "",
  newPassword: "",
  newPasswordConfirm: "",
});

const visible_1 = ref(false);
const visible_2 = ref(false);
const visible_3 = ref(false);

const alertMessage = ref("");
const alertVisible = ref(false);

const submit = async () => {
  try {
    await updatePassword(form.value);
  } catch (error) {
    if (error.response.status === 400) {
      alertMessage.value =
        "Trenutna lozinka nije ispravna" +
        " ili je nova lozinka ista kao trenutna";
      alertVisible.value = true;
    }
    console.log(error);
  }
};

if (!auth.isAuthenticated) router.push("/error/401");
else if (!auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <Background>
    <BackButton position="absolute" />
    <v-container fluid class="fill-height">
      <v-row class="justify-center align-center mb-16">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card border variant="flat" class="pa-4 my-12">
            <v-card-title class="text-center text-h5"
              >Unesite novu lozinku</v-card-title
            >
            <v-label
              class="text-subtitle-1 text-hard-emphasis"
              text="Trenutna lozinka"
            />
            <v-text-field
              :append-inner-icon="visible_1 ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible_1 ? 'text' : 'password'"
              density="compact"
              placeholder="Unesite trenutnu lozinku"
              variant="outlined"
              v-model="form.currentPassword"
              @click:append-inner="visible_1 = !visible_1"
              :rules="rules.currentPassword"
            ></v-text-field>

            <v-label
              class="text-subtitle-1 text-hard-emphasis"
              text="Nova lozinka"
            />
            <v-text-field
              :append-inner-icon="visible_2 ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible_2 ? 'text' : 'password'"
              density="compact"
              placeholder="Unesite novu lozinku"
              variant="outlined"
              v-model="form.newPassword"
              @click:append-inner="visible_2 = !visible_2"
              :rules="rules.password"
            ></v-text-field>

            <v-label
              class="text-subtitle-1 text-hard-emphasis"
              text="Potvrdi novu lozinku"
            />
            <v-text-field
              :append-inner-icon="visible_3 ? 'mdi-eye-off' : 'mdi-eye'"
              :type="visible_3 ? 'text' : 'password'"
              density="compact"
              placeholder="Unesite ponovno novu lozinku"
              variant="outlined"
              v-model="form.newPasswordConfirm"
              @click:append-inner="visible_3 = !visible_3"
              :rules="rules.passwordConfirm(form.newPassword)"
            ></v-text-field>

            <v-alert
              v-model="alertVisible"
              density="compact"
              variant="tonal"
              type="error"
              >{{ alertMessage }}</v-alert
            >

            <div class="d-flex pa-4 justify-space-evenly">
              <v-btn
                append-icon="mdi-check"
                color="blue-darken-2"
                variant="tonal"
                @click="submit"
                >Promijeni lozinku</v-btn
              >
              <v-btn
                append-icon="mdi-close"
                color="error"
                variant="tonal"
                @click="router.push('/account-management')"
                >Odustani</v-btn
              >
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </Background>
</template>

<style scoped></style>
