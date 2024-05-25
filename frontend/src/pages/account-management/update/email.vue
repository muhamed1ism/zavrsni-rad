<script setup>
import router from "@/router";
import { ref } from "vue";
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import { rules } from "@/components/FormValidationRules.vue";
import BackButton from "@/components/BackButton.vue";
import Background from "@/components/Background.vue";

const { auth } = useAuthStore();
const { user, updateEmail } = useUserStore();

const form = {
  email: user.email,
};

const alertMessage = ref("");
const alertVisible = ref(false);

const submit = async () => {
  try {
    await updateEmail(form.email);
  } catch (error) {
    if (error.response.status === 400) {
      alertMessage.value = "Nova email adresa ne smije biti ista kao stara";
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
              >Unesite novu email adresu</v-card-title
            >
            <v-label class="text-subtitle-1 text-hard-emphasis" text="Email" />
            <v-text-field
              density="compact"
              placeholder="Unesite email adresu"
              variant="outlined"
              v-model="form.email"
              :rules="rules.email"
            ></v-text-field>
            <v-alert
              v-model="alertVisible"
              density="compact"
              variant="tonal"
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
