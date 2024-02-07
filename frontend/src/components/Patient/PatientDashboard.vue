<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";

const authStore = useAuthStore();

if (!authStore.auth.hasProfile) {
  router.push("/patient/create");
}
</script>

<template>
  <v-container>
    <h1>Početna stranica pacijenta</h1>
    <p>Ovo je početna stranica pacijenta.</p>
  </v-container>
</template>

<style scoped></style>
