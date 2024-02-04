import { defineStore } from "pinia";
import axios from "axios";
import {useAuthStore} from "@/stores/useAuthStore";
import router from "@/router";

const apiUrl = "http://localhost:5003";

export const useAppointmentStore = defineStore("appointment", {
    state: () => ({
        appointments: [
            {
                id: null,
                patientId: null,
                doctorId: null,
                date: "",
                time: "",
                patientName: "",
                doctorName: "",
                createdAt: "",
                status: "",
            }
        ]
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

            if (res.status === 201) {
                await router.push("/appointments");
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

            if (res.status === 200) {
                this.appointments = res.data;
            }
        },

        async approveAppointment(appointmentId) {
            const approveAppointmentApiCall = () =>
                axios.put(`${apiUrl}/appointment/approve/${appointmentId}`,
                    appointmentId,{
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
            const res = await this.makeApiRequest(
                approveAppointmentApiCall,
                "Error setting appointment status"
            );

            if (res.status === 200) {
                await this.getAppointments();
            }
        },

        async rejectAppointment(appointmentId) {
            const rejectAppointmentApiCall = () =>
                axios.put(`${apiUrl}/appointment/reject/${appointmentId}`,
                    appointmentId, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
            const res = await this.makeApiRequest(
                rejectAppointmentApiCall,
                "Error setting appointment status"
            );

            if (res.status === 200) {
                await this.getAppointments();
            }
        },

        async cancelAppointment(appointmentId) {
            const cancelAppointmentApiCall = () =>
                axios.put(`${apiUrl}/appointment/cancel/${appointmentId}`,
                    appointmentId, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
            const res = await this.makeApiRequest(
                cancelAppointmentApiCall,
                "Failed to cancel appointment"
            );

            if (res.status === 200) {
                await this.getAppointments();
            }
        },
    },
});