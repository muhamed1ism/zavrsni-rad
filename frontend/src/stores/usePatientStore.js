import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const apiUrl = "http://localhost:5001";
const appointmentApiUrl = "http://localhost:5003";

export const usePatientStore = defineStore("patient", {
  state: () => ({
    patient: useLocalStorage("patient", {
      id: null,
      firstName: "",
      lastName: "",
      dateOfBirth: "",
      address: "",
      phoneNumber: "",
    }),
    patients: [],
  }),

  actions: {
    async createPatient(data) {
      try {
        const res = await axios.post(`${apiUrl}/create-patient`, data, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 201) {
          await this.getPatient();
          await router.push("/dashboard");
          window.location.reload();
        }
      } catch (error) {
        console.error("Failed to create patient: ", error);
        throw error;
      }
    },

    async getPatient() {
      try {
        const res = await axios.get(`${apiUrl}/get-patient`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 200) {
          this.patient = {
            id: res.data.id,
            firstName: res.data.firstName,
            lastName: res.data.lastName,
            dateOfBirth: res.data.dateOfBirth,
            address: res.data.address,
            phoneNumber: res.data.phoneNumber,
          };
          useAuthStore().auth.hasProfile = true;
        }
      } catch (error) {
        if (error.response.status === 404) {
          await router.push("/patient/create");
          window.location.reload();
        }
        console.error("Failed to get patient: ", error);
        throw error;
      }
    },

    async getPatients() {
        const res = await axios.get(`${appointmentApiUrl}/get-doctors-patients`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 200 && res.data.length > 0) {
          this.patients = res.data;
        }
    },

    async clearPatient() {
      try {
        this.patient = {
          id: "",
          firstName: "",
          lastName: "",
          dateOfBirth: "",
          address: "",
          phoneNumber: "",
        };
      } catch (error) {
        console.error("Failed to clear patient: " + error);
        throw error;
      }
    },

    async updatePatient(data) {
      try {
        const res = await axios.put(`${apiUrl}/update-patient`, data, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 200) {
          this.patient = data;
        }
      } catch (error) {
        console.error("Failed to update patient: ", error);
        throw error;
      }
    },
  },
});
