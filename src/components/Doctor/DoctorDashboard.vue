<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";

const authStore = useAuthStore();

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <h1>Početna stranica doktora</h1>
  <p>Ovo je početna stranica doktora.</p>
</template>

<style scoped></style>
