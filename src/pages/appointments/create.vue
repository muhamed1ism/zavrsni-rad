<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/useUserStore";
import {useAuthStore} from "@/stores/useAuthStore";
import {usePatientStore} from "@/stores/usePatientStore";
import {useAppointmentStore} from "@/stores/useAppointmentStore";

const form = ref({
  doctorId: "",
  date: "",
  time: "",
});

const userStore = useUserStore();
const authStore = useAuthStore();
const patientStore = usePatientStore();
const appointmentStore = useAppointmentStore();
const role = userStore.user.role;

const submit = async () => {
  try {
    await appointmentStore.createAppointment(form.value);

  } catch (error) {
    console.log(error);
  }
}
</script>

<template>
  <v-container class="fluid fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card border variant="flat" class="pa-4 mx-auto">
          <v-card-title class="text-center text-h5"
          >Naruči termin kod doktora</v-card-title
          >
          <v-card-item>
            <v-sheet>
              <v-form @submit.prevent="submit">
                <div class="text-subtitle-1 text-medium-emphasis">Odaberi doktora</div>
                <v-text-field
                    density="compact"
                    placeholder="Unesi ID doktora"
                    variant="outlined"
                    v-model="form.doctorId"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Odaberi datum</div>
                <v-text-field
                    density="compact"
                    placeholder="Unesi datum"
                    variant="outlined"
                    v-model="form.date"
                ></v-text-field>

                <div class="text-subtitle-1 text-medium-emphasis">Odaberi vrijeme</div>
                <v-text-field
                    density="compact"
                    placeholder="Unesi vrijeme"
                    variant="outlined"
                    v-model="form.time"
                ></v-text-field>

                <v-btn
                    border
                    block
                    type="submit"
                    variant="tonal"
                    color="blue-darken-2"
                    size="large"
                    class="mb-8 mt-2"
                >Naruči se</v-btn>
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