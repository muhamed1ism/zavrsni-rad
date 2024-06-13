<script setup>

import {ref} from "vue";

defineProps({
  appointments: Array,
  appointmentStore: Object,
});

const search = ref("");

const headers = [
  { title: "ID", text: "ID", value: "id", sortable: true },
  { title: "Doktor", text: "Doktor", value: "doctorName", sortable: true },
  { title: "Datum", text: "Datum", value: "date", sortable: true },
  { title: "Vrijeme", text: "Vrijeme", value: "time", sortable: true },
  { title: "Status", text: "Status", value: "status", sortable: true },
  {
    title: "Akcije",
    text: "Akcije",
    value: "actions",
    sortable: false,
    align: "center",
  },
];

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString("hr-HR");
};

const getColor = (status) => {
  if (status === "odobren") return "success";
  else if (status === "odbijen") return "error";
  else if (status === "na čekanju") return "warning";
};
</script>

<template>
  <v-container>
    <v-row class="d-flex align-center">
      <v-col>
        <h1 class="mb-4 my-4 mx-2 font-weight-medium">Moji naručeni termini</h1>
      </v-col>
      <v-col class="mb-4" cols="12" sm="5" lg="4">
        <v-text-field
            v-model="search"
            prepend-inner-icon="mdi-magnify"
            label="Pretraži"
            variant="outlined"
            density="compact"
            single-line
            hide-details
        />
      </v-col>
    </v-row>

    <v-card border elevation="0">
      <v-data-table
          :headers="headers"
          :items="appointments"
          :search="search"
          multi-sort
          items-per-page-text="Broj stavki po stranici"
          :items-per-page="10"
      >
        <template v-slot:item.date="{ item }">
          {{ item.date ? formatDate(item.date) : "" }}
        </template>
        <template v-slot:item.status="{ item }">
          <v-chip :color="getColor(item.status)">
            {{ item.status }}
          </v-chip>
        </template>
        <template v-slot:no-data>
          <p>Nema naručenih termina</p>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn
              v-if="item.id !== null && item.status === 'na čekanju'"
              prepend-icon="mdi-close"
              variant="tonal"
              color="error"
              width="100"
              @click="appointmentStore.cancelAppointment(item.id)"
          >
            Otkaži</v-btn
          >
          <v-btn
              v-else-if="item.id !== null && item.status === 'otkazan'"
              prepend-icon="mdi-check"
              variant="tonal"
              color="success"
              width="100"
              @click="appointmentStore.restoreAppointment(item.id)"
          >
            Vrati</v-btn
          >
        </template>
      </v-data-table>
    </v-card>
    <v-row class="mx-2 mt-4" justify="end">
      <v-btn
          to="/appointments/create"
          prepend-icon="mdi-calendar-plus"
          append-icon="mdi-arrow-right"
          variant="flat"
          elevation="0"
          text="Zakaži termin"
          size="large"
          border
      />
    </v-row>
  </v-container>
</template>

<style scoped>

</style>