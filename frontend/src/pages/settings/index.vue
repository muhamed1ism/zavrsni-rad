<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const authStore = useAuthStore();
const userStore = useUserStore();

const backgroundImage = "../../background.png";

const email = userStore.user.email;

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
} else if (!authStore.auth.hasProfile) {
  router.push("/dashboard")
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
                  to="/settings/update/email"
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
                  to="/settings/update/password"
                >
                </v-btn>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  </v-img>
</template>

<style scoped>

</style>
