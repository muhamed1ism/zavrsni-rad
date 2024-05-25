<template>
  <BackButton />
  <v-container>
    <h1 class="mb-4 my-4 mx-2 font-weight-medium">O nama</h1>
    <h3 class="mx-4 mb-4 font-weight-regular">Naša misija</h3>
    <p class="mx-6 mb-4 font-weight-light">
      Ovdje kratko opisujemo misiju naše kompanije i naših usluga.
    </p>

    <h3 class="mx-4 mb-4 font-weight-regular">Naš tim</h3>
    <p class="mx-6 mb-4 font-weight-light">
      Ovdje predstavljamo naš tim: tko smo, kakve su naše stručne vještine i što
      nas motivira.
    </p>

    <h3 class="mx-4 mb-4 font-weight-regular">Kako radimo</h3>
    <p class="mx-6 mb-4 font-weight-light">
      Ovdje opisujemo naš pristup radu: kako pružamo naše usluge, kako
      komuniciramo s klijentima, koje tehnologije koristimo itd.
    </p>

    <h3 class="mx-4 mb-4 font-weight-regular">Naša vizija</h3>
    <p class="mx-6 mb-4 font-weight-light">
      Ovdje iznosimo našu viziju i ciljeve za budućnost. Kako se vidimo u
      budućnosti i što očekujemo postići svojim radom.
    </p>
  </v-container>
</template>

<script setup>
import BackButton from "@/components/BackButton.vue";
</script>
