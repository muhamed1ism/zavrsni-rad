<script setup>
import { computed, ref } from "vue";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { rules } from "@/components/FormValidationRules.vue";
import router from "@/router";

const doctorStore = useDoctorStore();

const body = document.querySelector("body");
const isDark = localStorage.getItem("darkTheme") === "true";

const form = ref({
  firstName: doctorStore.doctor.firstName || "",
  lastName: doctorStore.doctor.lastName || "",
  specialty: doctorStore.doctor.specialty || "",
  address: doctorStore.doctor.address || "",
  phoneNumber: doctorStore.doctor.phoneNumber || "",
  dateOfBirth: doctorStore.doctor.dateOfBirth || null,
});

const maxDate = computed(() => {
  const date = new Date();
  date.setFullYear(date.getFullYear() - 18);
  return date;
});

const dateFormat = (date) => {
  return date.toLocaleDateString("hr-HR");
};

const submit = async () => {
  try {
    await doctorStore.updateDoctor(form.value);
    await router.push("/profile");
  } catch (error) {
    console.log(error);
  }
};
</script>

<template>
  <v-container fluid class="fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="5">
        <v-card border variant="flat" class="pa-4 my-12">
          <v-card-title class="text-center text-h5">Moji podaci</v-card-title>
          <v-card-item>
            <v-sheet>
              <v-form @submit.prevent="submit">
                <v-label
                  class="text-subtitle-1 text-hard-emphasis"
                  text="Ime"
                />
                <v-text-field
                  density="compact"
                  placeholder="Unesite ime"
                  variant="outlined"
                  v-model="form.firstName"
                  :rules="rules.firstName"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Prezime</div>
                <v-text-field
                  density="compact"
                  placeholder="Unesite prezime"
                  variant="outlined"
                  v-model="form.lastName"
                  :rules="rules.lastName"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Specijalnost
                </div>
                <v-text-field
                  density="compact"
                  placeholder="Unesite specijalnost"
                  variant="outlined"
                  v-model="form.specialty"
                  :rules="rules.specialty"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Adresa stanovanja
                </div>
                <v-text-field
                  density="compact"
                  placeholder="Unesite adresu stanovanja"
                  variant="outlined"
                  v-model="form.address"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Broj telefona
                </div>
                <v-text-field
                  density="compact"
                  placeholder="Unesite broj telefona"
                  variant="outlined"
                  v-model="form.phoneNumber"
                  :rules="rules.phoneNumber"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">
                  Datum rođenja
                </div>
                <v-container>
                  <v-row justify="center">
                    <VueDatePicker
                      v-model="form.dateOfBirth"
                      placeholder="Unesite datum rođenja"
                      :format="dateFormat"
                      locale="hr"
                      auto-apply
                      :enable-time-picker="false"
                      :teleport="body"
                      :dark="isDark"
                      :max-date="maxDate"
                    ></VueDatePicker>
                  </v-row>
                </v-container>

                <div class="v-input__details">
                  <div
                    class="v-messages"
                    role="alert"
                    aria-live="polite"
                    id="input-49-messages"
                  ></div>
                  <!---->
                </div>

                <v-btn
                  border
                  block
                  variant="tonal"
                  color="blue-darken-2"
                  size="large"
                  class="mb-8 mt-2"
                  @click="submit"
                  >Ažuriraj</v-btn
                >
              </v-form>
            </v-sheet>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
