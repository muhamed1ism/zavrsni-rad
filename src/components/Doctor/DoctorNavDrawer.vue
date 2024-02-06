<script setup>
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useUserStore } from "@/stores/useUserStore";

const doctorStore = useDoctorStore();
const userStore = useUserStore();
</script>

<template>
  <v-list color="blue-darken-2" nav>
    <v-list-item
      lines="two"
      prepend-avatar="https://api.dicebear.com/7.x/personas/svg?mouth=smile"
      :title="doctorStore.doctor.firstName + ' ' + doctorStore.doctor.lastName"
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
      to="/doctor"
      title="Moj profil"
    ></v-list-item>
    <v-list-item
      prepend-icon="mdi-calendar-clock"
      link
      to="/appointments"
      title="Lista naručenih pacijenta"
    ></v-list-item>
    <v-list-item
      prepend-icon="mdi-list-status"
      link
      to="/appointments/manage"
      title="Upravljaj terminima"
    ></v-list-item>
    <v-list-item
      prepend-icon="mdi-account-group-outline"
      link
      to="/patients"
      title="Moji pacijenti"
    ></v-list-item>
    <v-list-item
      prepend-icon="mdi-account-group"
      link
      to="/doctor/all"
      title="Doktori"
    ></v-list-item>
    <v-list-item
      prepend-icon="mdi-cog"
      link
      to="/settings"
      title="Postavke"
    ></v-list-item>
  </v-list>
</template>

<style scoped></style>
