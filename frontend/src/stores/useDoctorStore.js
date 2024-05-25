import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const apiUrl = "http://localhost:5002";

export const useDoctorStore = defineStore("doctor", {
  state: () => ({
    doctor: useLocalStorage("doctor", {
      id: "",
      firstName: "",
      lastName: "",
      specialty: "",
      dateOfBirth: "",
      address: "",
      phoneNumber: "",
    }),
    doctors: [],
  }),

  actions: {
    async createDoctor(data) {
      try {
        const res = await axios.post(`${apiUrl}/create-doctor`,
            data, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 201) {
          await this.getDoctor();
          await router.push("/dashboard");
          window.location.reload();
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          await this.createDoctor(data);
        }
        console.error("Failed to create doctor: " + error);
        throw error;
      }
    },

    async getDoctor() {
      try {
        const res = await axios.get(`${apiUrl}/get-doctor`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });

        if (res.status === 200) {
          this.doctor = {
            id: res.data.id,
            firstName: res.data.firstName,
            lastName: res.data.lastName,
            specialty: res.data.specialty,
            dateOfBirth: res.data.dateOfBirth,
            address: res.data.address,
            phoneNumber: res.data.phoneNumber,
          };
          useAuthStore().auth.hasProfile = true;
        }
      } catch (error) {
        if (error.response.status === 404) {
          await router.push("/profile/create");
          window.location.reload();
        }
        console.error("Failed to get doctor: " + error);
        throw error;
      }
    },

    async getDoctors() {
      try {
        const res = await axios.get(`${apiUrl}/get-doctors`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });

        if (res.status === 200) {
          this.doctors = res.data;
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          window.location.reload();
        }
        console.error("Failed to get doctors: " + error);
        throw error;
      }
    },

    async clearDoctor() {
      try {
        this.doctor = {
          id: "",
          firstName: "",
          lastName: "",
          specialty: "",
          dateOfBirth: "",
          address: "",
          phoneNumber: "",
        };
      } catch (error) {
        console.error("Failed to clear doctor: " + error);
        throw error;
      }
    },

    async updateDoctor(data) {
      try {
        data.dateOfBirth = new Date(data.dateOfBirth).toISOString();
        const res = await axios.put(`${apiUrl}/update-doctor`, data, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });

        if (res.status === 200) {
          await this.getDoctor();
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          await this.updateDoctor(data);
        }
        console.error("Failed to update doctor: " + error);
        throw error;
      }
    },
  },
});
