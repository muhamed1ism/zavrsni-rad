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
    async makeApiRequest(callback, errorMessage) {
      try {
        return await callback();
      } catch (error) {
        console.error(`${errorMessage}: `, error);
        throw error;
      }
    },

    async createPatient(data) {
      const createPatientApiCall = () =>
        axios.post(`${apiUrl}/create-patient`, data, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
      const res = await this.makeApiRequest(
        createPatientApiCall,
        "Failed to create patient",
      );

      if (res.status === 201) {
        await this.getPatient();
        await router.push("/dashboard");
      }
    },

    async getPatient() {
      const getPatientApiCall = () =>
        axios.get(`${apiUrl}/get-patient`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
      const res = await this.makeApiRequest(
        getPatientApiCall,
        "Failed to get patient",
      );

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
    },

    async getPatients() {
      const getPatientsApiCall = () =>
          axios.get(`${appointmentApiUrl}/get-doctors-patients`, {
            headers: {
              Authorization: "Bearer " + useAuthStore().auth.accessToken,
            },
          });
      const res = await this.makeApiRequest(
          getPatientsApiCall,
          "Error getting patients"
      );

      if (res.status === 200) {
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
      const updatePatientApiCall = () =>
        axios.put(`${apiUrl}/update-patient`, data, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
      const res = await this.makeApiRequest(
        updatePatientApiCall,
        "Failed to update patient",
      );

      if (res.status === 200) {
        this.patient = data;
      }
    },
  },
});
