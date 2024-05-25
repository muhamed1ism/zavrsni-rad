<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";
import BackButton from "@/components/BackButton.vue";

const { auth } = useAuthStore();
const { patients, getPatients } = usePatientStore();
const { user } = useUserStore();

getPatients();

const patientHeaders = [
  { title: "ID", value: "id", align: "start" },
  { title: "Ime", value: "name" },
  { title: "Adresa", value: "address" },
  { title: "Datum rođenja", value: "dateOfBirth" },
  { title: "Broj telefona", value: "phoneNumber" },
];

if (!auth.isAuthenticated) router.push("/error/401");
else if (user.role !== 'doctor') router.push("/error/403");
else if (!auth.hasProfile) router.push("/dashboard");
</script>

<template>
  <BackButton />
  <v-container>
    <h1 class="mb-4 my-4 mx-2 font-weight-medium">Moji pacijenti</h1>
    <v-card border elevation="0">
      <v-data-table
        :headers="patientHeaders"
        :items="patients"
        items-per-page-text="Broj stavki po stranici"
        :items-per-page="10"
      >
        <template v-slot:item.dateOfBirth="{ item }">
          {{
            item.dateOfBirth
              ? new Date(item.dateOfBirth).toLocaleDateString("hr-HR")
              : ""
          }}
        </template>
        <template v-slot:no-data>
          <p>Nema naručenih pacijenata</p>
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-2 mt-4" justify="end">
      <v-btn
        to="/doctors"
        prepend-icon="mdi-account-group"
        append-icon="mdi-arrow-right"
        variant="flat"
        elevation="0"
        text="Svi doktori"
        size="large"
        border
      />
    </v-row>
  </v-container>
</template>

<style scoped></style>
