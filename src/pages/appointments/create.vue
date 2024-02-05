<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/useUserStore";
import {useAuthStore} from "@/stores/useAuthStore";
import {useDoctorStore} from "@/stores/useDoctorStore";
import {useAppointmentStore} from "@/stores/useAppointmentStore";
import router from "@/router";

const form = ref({
  doctorId: "",
  date: null,
  time: "",
});

const userStore = useUserStore();
const authStore = useAuthStore();
const doctorStore = useDoctorStore();
const appointmentStore = useAppointmentStore();
const role = userStore.user.role;

doctorStore.getDoctors();

const submit = async () => {
  try {
    await appointmentStore.createAppointment(form.value);
  } catch (error) {
    console.log(error);
  }
}

if (!authStore.auth.isAuthenticated) {
  router.push("/login");
}

if (!authStore.auth.hasProfile) {
  router.push("/doctor/create");
}

if (role !== "patient") {
  console.log("Nemate pristup ovoj stranici");
  router.push("/dashboard");
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
                <v-select
                    v-model="form.doctorId"
                    :items="doctorStore.doctors"
                    :item-title="doctor => doctor.name"
                    :item-value="doctor => doctor.id"
                    variant="outlined"
                    density="compact"
                ></v-select>

                <v-container>
                  <v-row justify="center">
                    <v-locale-provider locale="hr">
                      <v-date-picker
                          width="100%"
                          v-model="form.date"
                          header="Datum termina"
                          border
                          title="Odaberi"
                      >
                      </v-date-picker>
                    </v-locale-provider>
                  </v-row>
                </v-container>

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