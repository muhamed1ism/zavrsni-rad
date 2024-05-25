<script setup>
import router from "@/router";
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import PatientProfileCreate from "@/components/Patient/Profile/PatientProfileCreate.vue";
import DoctorProfileCreate from "@/components/Doctor/Profile/DoctorProfileCreate.vue";
import Background from "@/components/Background.vue";

const { user } = useUserStore();
const { auth } = useAuthStore();

if (!auth.isAuthenticated) router.push("/login");
else if (auth.hasProfile) router.push("/dashboard");
</script>

<template>
  <Background>
    <PatientProfileCreate v-if="user.role === 'patient'" />
    <DoctorProfileCreate v-if="user.role === 'doctor'" />
  </Background>
</template>

<style scoped></style>