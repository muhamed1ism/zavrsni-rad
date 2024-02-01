import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import { useAuthStore } from "@/stores/useAuthStore";

const apiUrl = "http://localhost:5002";

export const useDoctorStore = defineStore("doctor", {
    state: () => ({
        doctor: useLocalStorage("doctor", {
            id: "",
            firstName: "",
            lastName: "",
            dateOfBirth: "",
            address: "",
            phoneNumber: "",
        }),
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

        async createDoctor(data) {
            const createDoctorApiCall = () =>
                axios.post(`${apiUrl}/create-doctor`,
                    data, {
                        headers: {
                            Authorization: "Bearer " + useAuthStore().auth.accessToken,
                        }
                    });
            const res = await this.makeApiRequest(
                createDoctorApiCall,
                "Failed to create doctor");

            if (res.status === 201) {
                await this.getDoctor();
                window.location.href = "/dashboard";
            }
        },

        async getDoctor() {
            const getDoctorApiCall = () =>
                axios.get(`${apiUrl}/get-doctor`, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    }
                });
            const res = await this.makeApiRequest(
                getDoctorApiCall,
                "Failed to get doctor"
            );

            if (res.status === 200) {
                this.doctor = {
                    id: res.data.id,
                    firstName: res.data.firstName,
                    lastName: res.data.lastName,
                    dateOfBirth: res.data.dateOfBirth,
                    address: res.data.address,
                    phoneNumber: res.data.phoneNumber,
                };
            }
        },

        async clearDoctor() {
            try {
                this.doctor = {
                    id: "",
                    firstName: "",
                    lastName: "",
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
            const updateDoctorApiCall = () =>
                axios.put(`${apiUrl}/update-doctor`,
                    data, {
                        headers: {
                            Authorization: "Bearer " + useAuthStore().auth.accessToken,
                        }
                    });
            const res = await this.makeApiRequest(
                updateDoctorApiCall,
                "Failed to update doctor"
            );

            if (res.status === 200) {
                this.doctor = data;
            }
        },
    },
});
