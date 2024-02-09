<template>
    <v-container class="text-center font-weight-light pt-16">
      <v-row class="justify-center align-center">
        <v-col class="v-col-auto">
        <v-img :src="image" class="mx-auto" width="400px" height="400px" alt="Logo"></v-img>
        </v-col>
        <v-col class="v-col-auto text-center text-lg-center">
          <h1 class="text-h2 font-weight-medium mb-3 ms-n1">eBolnica</h1>
          <p class="mb-10 mx-auto ms-lg-0">Dobrodošli u našu aplikaciju za <br> narudžbu pacijenata kod doktora!</p>
        </v-col>
      </v-row>
      <v-row class="justify-center pt-10">
        <v-col class="v-col-auto">
          <v-btn prepend-icon="mdi-chevron-right" variant="flat" density="default"
                 size="large" color="blue-darken-2" text="Započni" to="/login"/>
        </v-col>
        <v-col class="v-col-auto">
          <v-btn prepend-icon="mdi-information-outline" variant="outlined" density="default"
                 size="large" color="blue-darken-2" text="O nama" to="/about"/>
        </v-col>
        <v-col class="v-col-auto">
          <v-btn prepend-icon="mdi-github" variant="flat" density="default"
                 size="large" color="rgb(33, 33, 33)" text="GitHub" target="_blank"
                 href="https://github.com/muhamed1ism/zavrsni-rad"/>
        </v-col>
      </v-row>
    </v-container>
</template>

<script setup>
const image = "../../doctor.png"
</script>