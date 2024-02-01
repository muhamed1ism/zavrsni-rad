<script setup></script>

<template>
  <v-list-item link to="/dashboard" title="Početna stranica"></v-list-item>
  <v-divider></v-divider>
  <v-list-item link to="/profile" title="Moj profil"></v-list-item>
  <v-list-item
    link
    to="/appointments"
    title="Lista naručenih pacijenta"
  ></v-list-item>
  <v-list-item
    link
    to="/appointments/manage"
    title="Upravljaj terminima"
  ></v-list-item>
  <v-list-item link to="/patients" title="Moji pacijenti"></v-list-item>
  <v-list-item link to="/settings" title="Postavke"></v-list-item>
  <v-divider></v-divider>
</template>

<style scoped></style>
