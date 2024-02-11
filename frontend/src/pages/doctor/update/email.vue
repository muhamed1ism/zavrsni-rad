<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";
import { ref } from "vue";

const authStore = useAuthStore();
const userStore = useUserStore();
const email = userStore.user.email;

const backgroundImage = "../../background.png";

const form = {
  email: email,
};

const alertMessage = ref("");
const alertVisible = ref(false);

const emailRule = [
  (v) => !!v || "Email je obavezan",
  (v) => /.+@.+\..+/.test(v) || "Email mora biti validan",
];

const submit = async () => {
  try {
    await userStore.updateEmail(form.email);
  } catch (error) {
    if (error.response.status === 400) {
      alertMessage.value = "Nova email adresa ne smije biti ista kao stara";
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
          <v-card-title class="text-center text-h5"
            >Unesi novu email adresu</v-card-title
          >
          <div class="text-subtitle-1 text-medium-emphasis">Email</div>
          <v-text-field
            density="compact"
            placeholder="Email adresa"
            variant="outlined"
            v-model="form.email"
            :rules="emailRule"
          ></v-text-field>

          <v-alert
            v-if="alertVisible"
            v-model="alertVisible"
            density="compact"
            type="error"
            >{{ alertMessage }}
          </v-alert>

          <div class="d-flex pa-4 justify-space-evenly">
            <v-btn
              append-icon="mdi-check"
              color="blue-darken-2"
              variant="tonal"
              @click="submit"
              >Promijeni email</v-btn
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
  </v-img>
</template>

<style scoped>

</style>
