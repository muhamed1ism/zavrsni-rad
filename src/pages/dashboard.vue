<script setup>
  import PatientDashboard from "@/components/Patient/PatientDashboard.vue";
  import DoctorDashboard from "@/components/Doctor/DoctorDashboard.vue";
  import { useAuthStore } from "@/stores/useAuthStore";
  import { useUserStore } from "@/stores/useUserStore";
  import router from "@/router";

  const userStore = useUserStore();
  const authStore = useAuthStore();
  const role = userStore.user.role;

  if (!authStore.auth.isAuthenticated) {
    router.push("/login");
  }

  if (!authStore.auth.hasProfile) {
    router.push("/doctors/create");
  }
</script>

<template>
  <PatientDashboard v-if="role === 'patient'"></PatientDashboard>
  <DoctorDashboard v-else-if="role === 'doctor'"></DoctorDashboard>
</template>

<style scoped>

</style>