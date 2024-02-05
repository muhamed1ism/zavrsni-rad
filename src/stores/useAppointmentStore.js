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
        async createAppointment(data) {
            try {
                const res = await axios.post(`${apiUrl}/create-appointment`, data, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
                if (res.status === 201) {
                    await router.push("/appointments");
                }
            } catch (error) {
                console.error("Error creating appointment: ", error);
                throw error;
            }
        },

        async getAppointments() {
            try {
                const res = await axios.get(`${apiUrl}/get-all-appointments`, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
                if (res.status === 200 && res.data.length > 0) {
                    this.appointments = res.data;
                }
            } catch (error) {
                console.error("Error getting appointments: ", error);
                throw error;
            }
        },

        async approveAppointment(appointmentId) {
            try {
                const res = await axios.put(`${apiUrl}/appointment/approve/${appointmentId}`,
                    appointmentId,{
                        headers: {
                            Authorization: "Bearer " + useAuthStore().auth.accessToken,
                        },
                    });
                if (res.status === 200) {
                    await this.getAppointments();
                }
            } catch (error) {
                console.error("Error setting appointment status: ", error);
                throw error;
            }
        },

        async rejectAppointment(appointmentId) {
            try {
                const res = await axios.put(`${apiUrl}/appointment/reject/${appointmentId}`,
                    appointmentId, {
                        headers: {
                            Authorization: "Bearer " + useAuthStore().auth.accessToken,
                        },
                    });
                if (res.status === 200) {
                    await this.getAppointments();
                }
            } catch (error) {
                console.error("Error setting appointment status: ", error);
                throw error;
            }
        },

        async cancelAppointment(appointmentId) {
            try {
                const res = await axios.put(`${apiUrl}/appointment/cancel/${appointmentId}`,
                    appointmentId, {
                        headers: {
                            Authorization: "Bearer " + useAuthStore().auth.accessToken,
                        },
                    });
                if (res.status === 200) {
                    await this.getAppointments();
                }
            } catch (error) {
                console.error("Error setting appointment status: ", error);
                throw error;
            }
        },
    },
});