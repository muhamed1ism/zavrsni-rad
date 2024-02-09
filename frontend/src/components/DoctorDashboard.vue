<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/useAuthStore";

const authStore = useAuthStore();

const cards = [
  {
    title: "Odobrene narudžbe",
    style: "background-color: mediumseagreen",
    icon: "mdi-check",
    value: 0,
  },
  {
    title: "Narudžbe na čekanju",
    style: "background-color: darkgray",
    icon: "mdi-clock",
    value: 0,
  },
  {
    title: "Odbijene narudžbe",
    style: "background-color: indianred",
    icon: "mdi-close",
    value: 0,
  }
]

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}
</script>

<template>
  <v-container>
    <h1 class="mb-4 mt-2 mx-2">Nadzorna ploča doktora</h1>
    <v-row>
      <v-col cols="12" sm="6" lg="4" v-for="card in cards" :key="cards">
        <v-card>
          <v-row class="py-3">
            <v-col cols="4" class="d-flex justify-center align-center" :style="card.style">
              <v-icon>{{ card.icon }}</v-icon>
            </v-col>
            <v-col class="text-center">
              <v-card-title>{{ card.title }}</v-card-title>
              <v-card-item>{{ card.value }}</v-card-item>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6" lg="6">
        <h1>Pacijenti</h1>
        <v-data-table>
        </v-data-table>
      </v-col>
      <v-col>
        <h1>Narudžbe</h1>
        <v-data-table>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
