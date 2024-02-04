<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useDoctorsPatientStore } from "@/stores/useDoctorsPatientStore";
import {useUserStore} from "@/stores/useUserStore";
import router from "@/router";

const authStore = useAuthStore();
const doctorsPatientStore = useDoctorsPatientStore()
const userStore = useUserStore();
const role = userStore.user.role;

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/profile/create");
}


if (role !== "doctor") {
  console.log("Nemate pristup ovoj stranici");
  router.push("/dashboard");
}

doctorsPatientStore.getPatients();
</script>

<template>
  <h1>Moji pacijenti</h1>
  <table>
    <tr v-for="patient in doctorsPatientStore.patients" :key="patient.id">
      <td>{{patient.id}}</td>
      <td>{{patient.name}}</td>
    </tr>
  </table>
</template>

<style scoped>

</style>