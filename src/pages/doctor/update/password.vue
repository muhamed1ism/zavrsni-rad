<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const authStore = useAuthStore();
const userStore = useUserStore();

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

const newPasswordRule = [(v) => !!v || "Trenutna lozinka je obavezna"];

const passwordRule = [
  (v) => !!v || "Lozinka je obavezna",
  (v) => (v && v.length >= 8) || "Lozinka mora biti duža od 8 karaktera",
];

const passwordConfirmRule = [
  (v) => !!v || "Potvrda lozinke je obavezna",
  (v) => v === form.value.newPassword || "Lozinke se ne poklapaju",
];

const submit = async () => {
  try {
    await userStore.updatePassword(form.value);
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

const cancel = () => {
  router.push("/settings");
};

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5"
            >Unesi novu lozinku</v-card-title
          >
          <div class="text-subtitle-1 text-medium-emphasis">
            Trenutna lozinka
          </div>
          <v-text-field
            :append-inner-icon="visible_1 ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible_1 ? 'text' : 'password'"
            density="compact"
            placeholder=""
            variant="outlined"
            v-model="form.currentPassword"
            @click:append-inner="visible_1 = !visible_1"
            :rules="newPasswordRule"
          ></v-text-field>

          <div class="text-subtitle-1 text-medium-emphasis">Nova lozinka</div>
          <v-text-field
            :append-inner-icon="visible_2 ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible_2 ? 'text' : 'password'"
            density="compact"
            placeholder=""
            variant="outlined"
            v-model="form.newPassword"
            @click:append-inner="visible_2 = !visible_2"
            :rules="passwordRule"
          ></v-text-field>

          <div class="text-subtitle-1 text-medium-emphasis">
            Potvrdi novu lozinku
          </div>
          <v-text-field
            :append-inner-icon="visible_3 ? 'mdi-eye-off' : 'mdi-eye'"
            :type="visible_3 ? 'text' : 'password'"
            density="compact"
            placeholder=""
            variant="outlined"
            v-model="form.newPasswordConfirm"
            @click:append-inner="visible_3 = !visible_3"
            :rules="passwordConfirmRule"
          ></v-text-field>

          <v-alert
            v-if="alertVisible"
            v-model="alertVisible"
            density="compact"
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
              @click="cancel"
              >Odustani</v-btn
            >
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
