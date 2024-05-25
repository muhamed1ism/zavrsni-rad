<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";
import Background from "@/components/Background.vue";

const { auth } = useAuthStore();
const { user } = useUserStore();

const title = "Upravljanje računom";
const settings = [
  {
    title: "Email",
    value: `${user.email}`,
    route: "/account-management/update/email",
  },
  {
    title: "Password",
    value: "**********",
    route: "/account-management/update/password",
  },
];

if (!auth.isAuthenticated) router.push("/error/401");
else if (!auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <Background>
    <v-btn
      @click="router.go(-1)"
      size="large"
      class="mt-6 mx-4 elevation-0 border"
      position="absolute"
    >
      <v-icon icon="mdi-arrow-left" />
    </v-btn>
    <v-container fluid class="fill-height">
      <v-row class="justify-center align-center mb-16">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card border variant="flat" class="pt-4 pa-8 my-12">
            <v-card-title class="text-center text-h5 mb-6">{{
              title
            }}</v-card-title>
            <v-card-text v-for="item in settings" :key="item" class="">
              <v-label
                class="text-subtitle-1 text-hard-emphasis"
                :text="item.title"
              />
              <v-row>
                <v-col class="d-flex justify-center">
                  <v-text-field
                    disabled
                    readonly
                    density="compact"
                    variant="outlined"
                    :label="item.value"
                  />
                  <v-btn
                    class="ml-10"
                    color="blue-darken-2"
                    variant="tonal"
                    icon="mdi-pencil"
                    :to="item.route"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </Background>
</template>

<style scoped>
.v-card-text {
  padding: 0 !important;
}
</style>
