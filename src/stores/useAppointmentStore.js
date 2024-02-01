import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import {useAuthStore} from "@/stores/useAuthStore";

const apiUrl = "http://localhost:5003";

export const useAppointmentStore = defineStore("appointment", {
    state: () => ({
        appointment: useLocalStorage("appointment", {
            id: "",
            patientId: "",
            doctorId: "",
            date: "",
            time: "",
            patientName: "",
            doctorName: "",
            status: "",
            createdAt: "",
            updatedAt: "",
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

        async createAppointment(data) {
            const createAppointmentApiCall = () =>
                axios.post('${apiUrl}/appointments',
                    data, {
                        headers: {
                            Authorization: "Bearer " + useAuthStore().auth.accessToken,
                        }
                    });
            const res = await this.makeApiRequest(
                createAppointmentApiCall,
                "Error creating appointment"
            );

            if (res.status === 201) {
                console.log("Appointment created successfully");
            }
        },
    }
})