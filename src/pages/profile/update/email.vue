<script setup>

</script>

<template>
  <div class="text-subtitle-1 text-medium-emphasis">Email</div>
  <v-text-field
      density="compact"
      placeholder="Email adresa"
      variant="outlined"
      v-model="form.email"
      :rules="email_rule"
  ></v-text-field>
</template>

<style scoped>

</style>