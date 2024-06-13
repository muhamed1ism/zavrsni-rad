<script setup>
import { useUserStore } from "@/stores/useUserStore";
import PatientProfileUpdate from "@/components/Patient/Profile/PatientProfileUpdate.vue";
import DoctorProfileUpdate from "@/components/Doctor/Profile/DoctorProfileUpdate.vue";
import Background from "@/components/Background.vue";
import BackButton from "@/components/BackButton.vue";
import {useAuthStore} from "@/stores/useAuthStore";
import router from "@/router";

const userStore = useUserStore();
const authStore = useAuthStore();

if (!authStore.auth.isAuthenticated) router.push("/login");
else if (!authStore.auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <Background>
    <BackButton position="absolute" />
    <PatientProfileUpdate v-if="userStore.user.role === 'patient'" />
    <DoctorProfileUpdate v-if="userStore.user.role === 'doctor'" />
  </Background>
</template>

<style scoped></style>