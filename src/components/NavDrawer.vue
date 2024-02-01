<script setup>
import PatientNavDrawer from "@/components/Patient/PatientNavDrawer.vue";
import DoctorNavDrawer from "@/components/Doctor/DoctorNavDrawer.vue";
import {useUserStore} from "@/stores/useUserStore";

const userStore = useUserStore();
const role = userStore.user.role;
</script>

<template>
  <v-navigation-drawer location="left" temporary>
    <PatientNavDrawer v-if="role === 'patient'"></PatientNavDrawer>
    <DoctorNavDrawer v-else-if="role === 'doctor'"></DoctorNavDrawer>
    <div v-else>
      <v-list-item link to="/" title="Početna stranica"></v-list-item>
      <v-divider></v-divider>
      <v-list-item link to="login" title="Prijavi se"></v-list-item>
    </div>
    <v-list-item link to="profile/create">Napravi profile</v-list-item>
    <v-list-item link to="about" title="O nama"></v-list-item>
    <v-list-item link to="contact" title="Kontaktirajte nas"></v-list-item>
  </v-navigation-drawer>
</template>

<style scoped></style>
