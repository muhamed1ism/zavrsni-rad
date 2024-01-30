<script setup>
  import { ref } from "vue";
  import { useAuthStore } from "@/stores/useAuthStore";
  import {useUserStore} from "@/stores/useUserStore";

  const form = ref({
    email: "",
    password: "",
    password_confirm: "",
    role: "patient",
  });

  const visible = ref(false);

  const email_rule = [
    (v) => !!v || "Email je obavezan",
    (v) => /.+@.+/.test(v) || "Email nije validan",
  ];

  const password_rule = [
    (v) => !!v || "Lozinka je obavezna",
    (v) => (v && v.length >= 8) || "Lozinka mora biti duža od 8 karaktera",
  ];

  const password_confirm_rule = [
    (v) =>!!v || "Potvrda lozinke je obavezna",
    (v) => v === form.value.password || "Lozinke se ne poklapaju",
  ];

  const role_rule = [
    (v) =>!!v || "Role je obavezan",
  ];

  const authStore = useAuthStore();
  const userStore = useUserStore();

  const submit = async () => {
      await authStore.register(form.value.email, form.value.password, form.value.password_confirm, form.value.role);
      if (authStore.isAuthenticated) {
        console.log(localStorage.getItem("role") + " register success")
      }
  };

</script>

<template>
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5"
          >Registracija računa</v-card-title
          >
          <v-card-item>
            <v-sheet>
              <v-form @submit.prevent="submit">
                <div class="text-subtitle-1 text-medium-emphasis">Email</div>
                <v-text-field
                    density="compact"
                    placeholder="Email adresa"
                    variant="outlined"
                    v-model="form.email"
                    :rules="email_rule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Lozinka</div>
                <v-text-field
                    :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'"
                    density="compact"
                    placeholder="Unesite lozinku"
                    variant="outlined"
                    v-model="form.password"
                    @click:append-inner="visible = !visible"
                    :rules="password_rule"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Potvrdi lozinku
                </div>
                <v-text-field
                    :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'"
                    density="compact"
                    placeholder="Potvrdi lozinku"
                    variant="outlined"
                    v-model="form.password_confirm"
                    @click:append-inner="visible = !visible"
                    :rules="password_confirm_rule"
                ></v-text-field>

                <div class="mt-6 text-center text-subtitle-1 text-medium-emphasis">
                  Da li si pacijent ili doktor?
                </div>
                <v-container class="d-flex justify-center align-content-center">
                  <v-radio-group v-model="form.role" inline :rules="role_rule">
                    <v-container class="d-flex justify-space-evenly">
                    <v-radio label="Pacijent" color="blue" value="patient"></v-radio>
                    <v-radio label="Doktor" color="red" value="doctor"></v-radio>
                    </v-container>
                  </v-radio-group>
                </v-container>

                <v-btn
                    border
                    type="submit"
                    block
                    variant="tonal"
                    color="blue-darken-2"
                    size="large"
                    class="mb-8 mt-2"
                >Registriraj se</v-btn
                >
              </v-form>
            </v-sheet>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>

</style>