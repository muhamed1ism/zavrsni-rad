<script setup>
import router from "@/router";

</script>

<template>
  <v-btn
      @click="router.go(-1)"
      size="large"
      class="mt-6 mx-4 elevation-0 border"
  >
    <v-icon icon="mdi-arrow-left" />
  </v-btn>
</template>

<style scoped>

</style>