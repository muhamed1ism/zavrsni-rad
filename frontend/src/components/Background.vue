<script setup>
  const backgroundImage = "../../background.png";
</script>

<template>
  <v-img :src="backgroundImage" cover height="100%">
    <slot></slot>
  </v-img>
</template>

<style scoped>

</style>