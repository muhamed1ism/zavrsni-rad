<script setup>
import { useUserStore } from "@/stores/useUserStore";
import PatientProfile from "@/components/Patient/Profile/PatientProfile.vue";
import DoctorProfile from "@/components/Doctor/Profile/DoctorProfile.vue";
import Background from "@/components/Background.vue";
import BackButton from "@/components/BackButton.vue";

const { user } = useUserStore();
</script>

<template>
  <Background>
    <BackButton position="absolute" />
    <PatientProfile v-if="user.role === 'patient'" />
    <DoctorProfile v-if="user.role === 'doctor'" />
  </Background>
</template>

<style scoped></style>