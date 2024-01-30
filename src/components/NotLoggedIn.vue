<script setup>

</script>

<template>
  <v-container class="align-content-center">
    <div class="text-center text-medium-emphasis">
      <h1>Niste prijavljeni.</h1>
      <p>Molimo prijavite se kako biste pristupili ovoj funkcionalnosti.
        Ako nemate račun, možete se registrirati.</p>
    </div>
    <div class="d-flex justify-space-evenly">
      <v-btn @click="$router.push('/')">Početna stranica</v-btn>
      <v-btn @click="$router.push('/register')">Registrirajte se</v-btn>
      <v-btn @click="$router.push('/login')">Prijavite se</v-btn>
    </div>
  </v-container>

</template>

<style scoped>

</style>