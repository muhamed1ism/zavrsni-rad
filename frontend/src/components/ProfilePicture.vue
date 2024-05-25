<script setup>

 const profilePicture = '';
 defineProps({
   pictureSize: String
 })

</script>

<template>
  <v-avatar :size="pictureSize">
    <v-img v-if="profilePicture" :size="pictureSize"  :src="profilePicture"/>
    <v-icon v-else :size="pictureSize">mdi-account-circle</v-icon>
  </v-avatar>
</template>

<style scoped>

</style>