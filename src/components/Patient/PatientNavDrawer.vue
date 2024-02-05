<script setup>
import { useUserStore } from "@/stores/useUserStore";
import { usePatientStore } from "@/stores/usePatientStore";

const userStore = useUserStore();
const patientStore = usePatientStore();
</script>

<template>
  <v-list-item
    lines="two"
    prepend-avatar="https://api.dicebear.com/7.x/personas/svg?mouth=smile"
    :title="patientStore.patient.firstName + ' ' + patientStore.patient.lastName"
    :subtitle="userStore.user.email"
  >
  </v-list-item>
  <v-divider></v-divider>
  <v-list-item
    prepend-icon="mdi-view-dashboard"
    link
    to="/dashboard"
    title="Početna stranica"
  ></v-list-item>
  <v-list-item
    prepend-icon="mdi-account"
    link
    to="/patient"
    title="Moj profil"
  ></v-list-item>
  <v-list-item
    prepend-icon="mdi-account-group"
    link
    to="/doctor/all"
    title="Doktori"
  ></v-list-item>
  <v-list-item
    prepend-icon="mdi-calendar-clock"
    link
    to="/appointments"
    title="Moji termini"
  ></v-list-item>
  <v-list-item
    prepend-icon="mdi-calendar-plus"
    link
    to="/appointments/create"
    title="Naruči termin"
  ></v-list-item>
  <v-list-item
    prepend-icon="mdi-cog"
    link
    to="/settings"
    title="Postavke"
  ></v-list-item>
  <v-divider></v-divider>
</template>

<style scoped></style>
