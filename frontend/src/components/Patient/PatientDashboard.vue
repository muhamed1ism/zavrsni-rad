<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";

const authStore = useAuthStore();

if (!authStore.auth.hasProfile) {
  router.push("/patient/create");
}
</script>

<template>
  <h1>Početna stranica pacijenta</h1>
  <p>Ovo je početna stranica pacijenta.</p>
</template>

<style scoped></style>
