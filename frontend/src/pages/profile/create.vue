<script setup>
import router from "@/router";
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import PatientProfileCreate from "@/components/Patient/Profile/PatientProfileCreate.vue";
import DoctorProfileCreate from "@/components/Doctor/Profile/DoctorProfileCreate.vue";
import Background from "@/components/Background.vue";

const userStore = useUserStore();
const authStore = useAuthStore();

if (!authStore.auth.isAuthenticated) router.push("/login");
if (authStore.auth.hasProfile) router.push("/dashboard");
</script>

<template>
  <Background>
    <PatientProfileCreate v-if="userStore.user.role === 'patient'" />
    <DoctorProfileCreate v-if="userStore.user.role === 'doctor'" />
  </Background>
</template>

<style scoped></style>