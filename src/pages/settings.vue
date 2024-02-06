<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const authStore = useAuthStore();
const userStore = useUserStore();
const email = userStore.user.email;
const role = userStore.user.role;

const emailAction = () => {
  if (role === "patient") {
    router.push("/patient/update/email");
  } else if (role === "doctor") {
    router.push("/doctor/update/email");
  }
};

const passwordAction = () => {
  if (role === "patient") {
    router.push("/patient/update/password");
  } else if (role === "doctor") {
    router.push("/doctor/update/password");
  }
};

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  if (role === "patient") {
    router.push("/patient/create");
  } else if (role === "doctor") {
    router.push("/doctor/create");
  }
}
</script>

<template>
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5">Postavke</v-card-title>
          <v-card-text class="mt-6">
            <div class="my-2">
              <div class="text-subtitle-1 text-medium-emphasis">Email</div>
              <div class="d-flex align-center">
                <p>{{ email }}</p>
                <v-btn
                  class="ml-10"
                  color="blue-darken-2"
                  variant="tonal"
                  icon="mdi-pencil"
                  @click="emailAction"
                >
                </v-btn>
              </div>
            </div>

            <div class="my-2">
              <div class="text-subtitle-1 text-medium-emphasis">Password</div>
              <div class="d-flex align-center">
                <p>**********</p>
                <v-btn
                  class="ml-10"
                  color="blue-darken-2"
                  variant="tonal"
                  icon="mdi-pencil"
                  @click="passwordAction"
                >
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
