<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";

const form = ref({
  email: "",
  password: "",
});

const email_rule = [
  (v) => !!v || "Email je obavezan",
  (v) => /.+@.+/.test(v) || "Email nije validanog formata",
];

const password_rule = [
  (v) => !!v || "Lozinka je obavezna",
  (v) => v.length >= 8 || "Lozinka mora imati najmanje 8 karaktera",
];

const visible = ref(false);

const authStore = useAuthStore();

const submit = async () => {
  try {
    await authStore.login(form.value);
  } catch (error) {
    console.log(error);
  }
};
</script>

<template>
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5">Prijava</v-card-title>
          <v-card-item>
            <v-sheet>
              <v-form @submit.prevent="submit">
                <div class="text-subtitle-1 text-medium-emphasis">Email</div>

                <v-text-field
                    density="compact"
                    placeholder="Email adresa"
                    prepend-inner-icon="mdi-email-outline"
                    variant="outlined"
                    v-model="form.email"
                    :rules="email_rule"
                ></v-text-field>

                <div
                    class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
                >
                  Lozinka
                </div>

                <v-text-field
                    :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'"
                    density="compact"
                    placeholder="Unesite lozinku"
                    prepend-inner-icon="mdi-lock-outline"
                    variant="outlined"
                    v-model="form.password"
                    @click:append-inner="visible = !visible"
                    :rules="password_rule"
                ></v-text-field>

                <v-btn
                    border
                    type="submit"
                    block
                    variant="tonal"
                    color="blue-darken-2"
                    size="large"
                    class="mb-8 mt-2"
                >Prijavi se</v-btn
                >

                <v-card-text class="text-center">
                  <a
                      class="text-blue-darken-2 text-decoration-none"
                      href="/register"
                  >Napravi račun <v-icon icon="mdi-chevron-right"></v-icon>
                  </a>
                </v-card-text>
              </v-form>
            </v-sheet>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>