<script setup>
import { useDoctorStore } from "@/stores/useDoctorStore";
import ProfilePicture from "@/components/ProfilePicture.vue";
import { onMounted } from "vue";

const doctorStore = useDoctorStore();

onMounted(async () => {
  await doctorStore.getDoctor();
});

const doctorDateOfBirth = new Date(doctorStore.doctor.dateOfBirth).toLocaleDateString(
  "hr-HR",
);

const title = "Moji podaci";
const doctorName = [
  {
    title: "Ime",
    value: `${doctorStore.doctor.firstName}`,
  },
  {
    title: "Prezime",
    value: `${doctorStore.doctor.lastName}`,
  },
]
const doctorData = [
  {
    title: "Specijalnost",
    value: `${doctorStore.doctor.specialty}`,
  },
  {
    title: "Adresa",
    value: `${doctorStore.doctor.address}`,
  },
  {
    title: "Broj telefona",
    value: `${doctorStore.doctor.phoneNumber}`,
  },
  {
    title: "Datum rođenja",
    value: `${doctorDateOfBirth}`,
  },
];
</script>

<template>
  <v-container fluid class="fill-height">
    <v-row class="justify-center align-center mb-16">
      <v-col cols="12" sm="8" md="6" lg="5">
        <v-card border variant="flat" :min-width="$vuetify.display.smAndUp ? '470' : ''" class="pa-4 my-12">
          <v-card-title class="text-center text-h5">{{ title }}</v-card-title>
          <v-card-item>
            <v-row class="justify-center align-center">
              <v-col cols="12" md="5" lg="4" class="d-flex justify-space-around align-center">
              <ProfilePicture picture-size="140"/>
              </v-col>
              <v-col class="pb-0">
                <v-card-text
                    v-for="item in doctorName"
                    :key="item"
                    class="v-card-text"
                >
                  <v-label
                      class="text-subtitle-1 text-hard-emphasis"
                      :text="item.title"
                  />
                  <v-text-field
                      disabled
                      readonly
                      density="compact"
                      variant="outlined"
                  >{{ item.value }}</v-text-field
                  >
                </v-card-text>
              </v-col>
              <v-col cols="12">
                <v-card-text
                    v-for="item in doctorData"
                    :key="item"
                    class="v-card-text"
                >
                  <v-label
                      class="text-subtitle-1 text-hard-emphasis"
                      :text="item.title"
                  />
                  <v-text-field
                      disabled
                      readonly
                      density="compact"
                      variant="outlined"
                  >{{ item.value }}</v-text-field
                  >
                </v-card-text>
                <v-btn
                    border
                    block
                    size="large"
                    class="mb-8 mt-6"
                    color="blue-darken-2"
                    variant="tonal"
                    append-icon="mdi-pencil"
                    :to="`/profile/update`"
                    text="Uredi"
                />
              </v-col>
            </v-row>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.v-card-text {
  padding: 0 !important;
}
</style>
