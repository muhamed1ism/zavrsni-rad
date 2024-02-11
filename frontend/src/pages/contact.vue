<script setup>
import router from "@/router";
</script>

<template>
  <v-container>
    <v-btn
        @click="router.go(-1)"
        size="large"
        class="mt-2 mx-2">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>
    <h1 class="mb-6 mt-4 mx-2 font-weight-medium">Kontaktirajte nas</h1>
    <h3 class="mx-4 font-weight-regular">Cijenimo vaše mišljenje i feedback.</h3>

    <p class="mx-6 mb-4 font-weight-light">
      Za bilo kakva pitanja, prijedloge ili komentare, ne oklijevajte se obratiti. <br>
      Možete nas kontaktirati putem e-maila na <strong>email@example.com</strong> <br>
      ili na telefon <strong>+387 61 234 5678</strong>. <br>
      Radujemo se vašem upitu!
    </p>
  </v-container>
</template>

<style scoped></style>
