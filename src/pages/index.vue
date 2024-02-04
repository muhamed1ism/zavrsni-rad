<template>
  <div>
    Početna stranica aplikacije
  </div>
</template>

<script setup>
  import { useAuthStore } from "@/stores/useAuthStore";
  import router from "@/router";

  const authStore = useAuthStore();

  if (authStore.auth.isAuthenticated) {
    router.push("/dashboard");
  }
</script>
