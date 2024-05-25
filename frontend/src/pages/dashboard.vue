<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";
import { useUserStore } from "@/stores/useUserStore";
import DoctorDashboard from "@/components/Doctor/DoctorDashboard.vue";
import PatientDashboard from "@/components/Patient/PatientDashboard.vue";

const { user } = useUserStore();
const { auth } = useAuthStore();

if (!auth.isAuthenticated) router.push("/login");
else if (!auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <PatientDashboard v-if="user.role === 'patient'"></PatientDashboard>
  <DoctorDashboard v-else-if="user.role === 'doctor'"></DoctorDashboard>
</template>

<style scoped></style>
