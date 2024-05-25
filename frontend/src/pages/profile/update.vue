<script setup>
import { useUserStore } from "@/stores/useUserStore";
import PatientProfileUpdate from "@/components/Patient/Profile/PatientProfileUpdate.vue";
import DoctorProfileUpdate from "@/components/Doctor/Profile/DoctorProfileUpdate.vue";
import Background from "@/components/Background.vue";
import BackButton from "@/components/BackButton.vue";

const { user } = useUserStore();
</script>

<template>
  <Background>
    <BackButton position="absolute" />
    <PatientProfileUpdate v-if="user.role === 'patient'" />
    <DoctorProfileUpdate v-if="user.role === 'doctor'" />
  </Background>
</template>

<style scoped></style>