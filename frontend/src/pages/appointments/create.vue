<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/useUserStore";
import { useAuthStore } from "@/stores/useAuthStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import { useAppointmentStore } from "@/stores/useAppointmentStore";
import router from "@/router";
import BackButton from "@/components/BackButton.vue";
import Background from "@/components/Background.vue";

const form = ref({
  doctorId: "",
  date: null,
  time: "",
});

const { user } = useUserStore();
const { auth } = useAuthStore();
const { doctors, getDoctors } = useDoctorStore();
const { createAppointment } = useAppointmentStore();

const isDark = localStorage.getItem("darkTheme") === "true";
const body = document.querySelector("body");

getDoctors();

const dateFormat = (date) => {
  return date.toLocaleDateString("hr-HR");
};

const disabledTimes = [
  ...Array.from({ length: 8 }, (v, i) => ({ hours: i, minutes: "*" })),
  { hours: 11, minutes: "*" },
  ...Array.from({ length: 9 }, (v, i) => ({ hours: i + 16, minutes: "*" })),
];

const submit = async () => {
  try {
    await createAppointment(form.value);
  } catch (error) {
    console.log(error);
  }
};

if (!auth.isAuthenticated) router.push("/error/401");
else if (user.role !== "patient") router.push("/error/403")
else if (!auth.hasProfile)  router.push("/profile/create");
</script>

<template>
  <Background>
    <BackButton position="absolute" />
    <v-container fluid class="fill-height d-flex justify-center align-center">
      <v-row class="justify-center align-center mb-16">
        <v-col cols="12" sm="8" md="5">
          <v-card border variant="flat" class="pa-4 my-12">
            <v-card-title
              class="text-center"
              :class="$vuetify.display.smAndUp ? 'text-h5' : ''"
            >
              Naruči termin kod doktora
            </v-card-title>
            <v-card-item>
              <v-sheet>
                <v-form @submit.prevent="submit">
                  <v-label
                    class="text-subtitle-1 text-hard-emphasis"
                    text="Doktor"
                  />
                  <v-select
                    v-model="form.doctorId"
                    :items="doctors"
                    :item-title="
                      (doctor) => doctor.specialty + ' - ' + doctor.name
                    "
                    :item-value="(doctor) => doctor.id"
                    prepend-inner-icon="mdi-doctor"
                    variant="outlined"
                    density="compact"
                  >
                    <template #selection="{ item }" v-if="form.doctorId === ''">
                      <v-label>Odaberi doktora</v-label>
                    </template>
                  </v-select>

                  <v-label
                    class="text-subtitle-1 text-hard-emphasis"
                    text="Datum termina"
                  />
                  <VueDatePicker
                    class="mb-6"
                    v-model="form.date"
                    placeholder="Unesite datum termina"
                    :format="dateFormat"
                    locale="hr"
                    auto-apply
                    disable-year-select
                    :enable-time-picker="false"
                    :teleport="body"
                    :dark="isDark"
                    :min-date="new Date()"
                    :disabled-week-days="[6, 0]"
                  ></VueDatePicker>

                  <v-label
                    class="text-subtitle-1 text-hard-emphasis"
                    text="Odaberi vrijeme"
                  />
                  <VueDatePicker
                    class="mb-10"
                    placeholder="Unesite vrijeme"
                    v-model="form.time"
                    locale="hr"
                    :teleport="body"
                    time-picker
                    :disabled-times="disabledTimes"
                    :dark="isDark"
                  >
                    <template #input-icon>
                      <v-icon class="dp__input_icons d-flex"
                        >mdi-clock-time-four-outline</v-icon
                      >
                    </template>
                  </VueDatePicker>

                  <v-btn
                    border
                    block
                    type="submit"
                    variant="tonal"
                    color="blue-darken-2"
                    size="large"
                    class="mb-4"
                    >Naruči se</v-btn
                  >
                </v-form>
              </v-sheet>
            </v-card-item>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </Background>
</template>

<style scoped></style>
