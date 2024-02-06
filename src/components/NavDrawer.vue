<script setup>
import PatientNavDrawer from "@/components/Patient/PatientNavDrawer.vue";
import DoctorNavDrawer from "@/components/Doctor/DoctorNavDrawer.vue";
import { useUserStore } from "@/stores/useUserStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useAuthStore } from "@/stores/useAuthStore";

const authStore = useAuthStore();
const userStore = useUserStore();
const patientStore = usePatientStore();
const doctorStore = useDoctorStore();

const role = userStore.user.role;
</script>

<template>
  <v-navigation-drawer width="300" location="left" temporary>
    <PatientNavDrawer v-if="role === 'patient'"></PatientNavDrawer>
    <DoctorNavDrawer v-else-if="role === 'doctor'"></DoctorNavDrawer>
    <div v-else>
      <v-list color="blue-darken-2" nav>
        <v-list-item
          prepend-icon="mdi-home"
          link
          to="/"
          title="Početna stranica"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-login"
          link
          to="/login"
          title="Prijavi se"
        ></v-list-item>
      </v-list>
    </div>
    <v-list color="blue-darken-2" nav>
      <v-divider></v-divider>
      <v-list-item
        prepend-icon="mdi-information"
        link
        to="/about"
        title="O nama"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-phone"
        link
        to="/contact"
        title="Kontaktirajte nas"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped></style>
