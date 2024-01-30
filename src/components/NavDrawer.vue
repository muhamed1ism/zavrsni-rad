<script setup>
import PatientNavDrawer from "@/components/Patient/PatientNavDrawer.vue";
import DoctorNavDrawer from "@/components/Doctor/DoctorNavDrawer.vue";

const isPatient = localStorage.getItem("role") === "patient";
const isDoctor = localStorage.getItem("role") === "doctor";
</script>

<template>
  <v-navigation-drawer location="left" temporary>
    <PatientNavDrawer v-if="isPatient"></PatientNavDrawer>
    <DoctorNavDrawer v-else-if="isDoctor"></DoctorNavDrawer>
    <div v-else>
      <v-list-item link to="/" title="Početna stranica"></v-list-item>
      <v-divider></v-divider>
      <v-list-item link to="login" title="Prijavi se"></v-list-item>
    </div>
    <v-list-item link to="about" title="O nama"></v-list-item>
    <v-list-item link to="contact" title="Kontaktirajte nas"></v-list-item>
  </v-navigation-drawer>
</template>

<style scoped></style>
