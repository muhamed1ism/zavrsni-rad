<script setup>

import BackButton from "@/components/BackButton.vue";
</script>

<template>
  <BackButton position="absolute" />
  <v-container fluid class="fill-height">
    <v-row>
      <v-col>
        <h1 class="text-h1 text-center text-medium-emphasis">Error 401</h1>
        <p class="text-h2 text-center text-medium-emphasis">Nemate ovlašten pristup ovoj stranici</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>

</style>