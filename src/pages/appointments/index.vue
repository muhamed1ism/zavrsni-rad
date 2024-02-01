<script setup>

import {useAppointmentStore} from "@/stores/useAppointmentStore";
import {onMounted} from "vue";

const appointmentStore = useAppointmentStore();

onMounted(() => {
  appointmentStore.getAppointments();
});
</script>

<template>
  <h1>Termini pacijenta/pacijenata - za doktora i pacijenta ruta</h1>
  <table>
    <tr v-for="appointment in appointmentStore.appointments" :key="appointment.id">
      <td>{{appointment.id}}</td>
      <td>{{appointment.doctorId}}</td>
      <td>{{appointment.patientId}}</td>
      <td>{{appointment.date}}</td>
      <td>{{appointment.time}}</td>
      <td>{{appointment.status}}</td>
    </tr>
  </table>
</template>

<style scoped>

</style>