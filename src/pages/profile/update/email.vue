<script setup>
import { useUserStore } from "@/stores/useUserStore";

const userStore = useUserStore();
const email = userStore.user.email || "";

const form = {
  email: `${email}`,
};

const emailRule = [
  (v) => !!v || "Email je obavezan",
  (v) => /.+@.+\..+/.test(v) || "Email mora biti validan",
];

const submit = async () => {
  try {
    await userStore.updateEmail(form);
  } catch (error) {
    console.log(error);
  }
};

const cancel = () => {
  window.location.href = "/settings";
};
</script>

<template>
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
          <div class="d-flex pa-4 justify-space-evenly">
            <v-btn
              append-icon="mdi-check"
              color="primary"
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
</template>

<style scoped></style>