<template>
  <v-container>
    <h1>Početna stranica aplikacije, dok korisnik nije prijavljen</h1>
  </v-container>
</template>

<script setup>
  import { useAuthStore } from "@/stores/useAuthStore";
  import router from "@/router";

  const authStore = useAuthStore();

  if (authStore.auth.isAuthenticated) {
    router.push("/dashboard");
  }
</script>
