<script setup>
import {onMounted, ref, watch} from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useUserStore } from "@/stores/useUserStore";
import router from "@/router";
import BackButton from "@/components/BackButton.vue";

const doctors = ref([]);
const search = ref("");

const authStore = useAuthStore();
const userStore = useUserStore();
const doctorStore = useDoctorStore();

onMounted(async () => {
  await doctorStore.getDoctors();
  doctors.value = doctorStore.doctors;
});

watch(
  () => doctorStore.doctors,
  (newDoctors) => {
    doctors.value = newDoctors;
  }
);

const doctorHeaders = [
  { title: "ID", value: "id", align: "start", sortable: true },
  { title: "Name", value: "name", sortable: true },
  {
    title: "Specialty",
    value: "specialty",
    sortable: true
  },
];

if (!authStore.auth.isAuthenticated) router.push("/error/401");
else if (!authStore.auth.hasProfile) router.push("/profile/create");
</script>

<template>
  <BackButton />
  <v-container>
    <v-row class="d-flex align-center">
      <v-col>
        <h1 class="mb-4 my-4 mx-2 font-weight-medium">Doctors</h1>
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
        :headers="doctorHeaders"
        :items="doctors"
        :search="search"
        multi-sort
        :items-per-page="10"
      >
        <template v-slot:no-data>
          <p>No doctors</p>
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-2 mt-4" justify="end">
      <v-btn
        v-if="userStore.user.role === 'doctor'"
        to="/patients"
        prepend-icon="mdi-account-group"
        append-icon="mdi-arrow-right"
        variant="flat"
        elevation="0"
        text="My patients"
        size="large"
        border
      />
      <v-btn
        v-if="userStore.user.role === 'patient'"
        to="/appointments"
        prepend-icon="mdi-calendar-clock"
        append-icon="mdi-arrow-right"
        variant="flat"
        elevation="0"
        text="My appointments"
        size="large"
        border
      />
    </v-row>
  </v-container>
</template>

<style scoped></style>
