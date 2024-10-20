<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";
import BackButton from "@/components/BackButton.vue";
import {onMounted, ref, watch} from "vue";

const patients = ref([]);
const search = ref("");

const authStore = useAuthStore();
const patientsStore = usePatientStore();
const userStore = useUserStore();

onMounted(async () => {
  await patientsStore.getPatients();
  patients.value = patientsStore.patients;
});

watch(
  () => patientsStore.patients,
  (newPatients) => {
    patients.value = newPatients;
  }
)

const patientHeaders = [
  { title: "ID", value: "id", align: "start", sortable: true },
  { title: "Name", value: "name", sortable: true },
  { title: "Address", value: "address", sortable: true },
  { title: "Date of birth", value: "dateOfBirth", sortable: true },
  { title: "Phone number", value: "phoneNumber", sortable: true },
];

if (!authStore.auth.isAuthenticated) router.push("/error/401");
else if (userStore.user.role !== 'doctor') router.push("/error/403");
else if (!authStore.auth.hasProfile) router.push("/dashboard");
</script>

<template>
  <BackButton />
  <v-container>
    <v-row class="d-flex align-center">
      <v-col>
        <h1 class="mb-4 my-4 mx-2 font-weight-medium">My patients</h1>
      </v-col>
      <v-col class="mb-4" cols="12" sm="5" lg="4">
        <v-text-field
            v-model="search"
            prepend-inner-icon="mdi-magnify"
            label="Search"
            variant="outlined"
            density="compact"
            single-line
            hide-details
        />
      </v-col>
    </v-row>

    <v-card border elevation="0">
      <v-data-table
        :headers="patientHeaders"
        :items="patients"
        :search="search"
        multi-sort
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
          <p>No patients</p>
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
        text="Doctors"
        size="large"
        border
      />
    </v-row>
  </v-container>
</template>

<style scoped></style>
