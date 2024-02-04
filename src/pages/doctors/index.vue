<script setup>

import { useAuthStore } from "@/stores/useAuthStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import {useUserStore} from "@/stores/useUserStore";
import router from "@/router";

const authStore = useAuthStore();
const doctorStore = useDoctorStore();
const userStore = useUserStore();
const role = userStore.user.role;

if (!authStore.auth.isAuthenticated){
  router.push("/login");
}

if (!authStore.auth.hasProfile){
  router.push("/profile/create");
}

if (role !== "patient") {
  console.log("Nemate pristup ovoj stranici");
  router.push("/dashboard");
}

doctorStore.getDoctors();

const headers = [
  { title: "ID", text: "ID", value: "id", align: "start"},
  { title: "Ime", text: "Ime", value: "name", align: "center"},
]
</script>

<template>
  <h1>Doktori</h1>
  <v-container>
    <v-data-table

        :headers="headers"
        :items="doctorStore.doctors"
        :items-per-page="10"
        class="elevation-1"
    >
    </v-data-table>
  </v-container>
</template>

<style scoped>
</style>