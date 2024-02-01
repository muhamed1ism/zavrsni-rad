import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import {useAuthStore} from "@/stores/useAuthStore";

const apiUrl = "http://localhost:5003";

export const useAppointmentStore = defineStore("appointment", {
    state: () => ({
        appointments: []
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

        async createAppointment(data) {
            const createAppointmentApiCall = () =>
                axios.post(`${apiUrl}/create-appointment`, data, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
            const res = await this.makeApiRequest(
                createAppointmentApiCall,
                "Error creating appointment"
            );

            if (res?.status === 201) {
                window.location.href = "/appointments";
            }
        },

        async getAppointments() {
            const getAppointmentsApiCall = () =>
                axios.get(`${apiUrl}/get-all-appointments`, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
            const res = await this.makeApiRequest(
                getAppointmentsApiCall,
                "Error getting appointments"
            );

            if (res?.status === 200) {
                this.appointments = res.data;
            }
        }

    },
});