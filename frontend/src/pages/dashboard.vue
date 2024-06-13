<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";
import { useUserStore } from "@/stores/useUserStore";
import DoctorDashboard from "@/components/Doctor/DoctorDashboard.vue";
import PatientDashboard from "@/components/Patient/PatientDashboard.vue";

const userStore = useUserStore();
const authStore = useAuthStore();

if (!authStore.auth.isAuthenticated) router.push("/login");
else if (!authStore.auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <PatientDashboard v-if="userStore.user.role === 'patient'"></PatientDashboard>
  <DoctorDashboard v-else-if="userStore.user.role === 'doctor'"></DoctorDashboard>
</template>

<style scoped></style>
