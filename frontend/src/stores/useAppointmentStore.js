import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";

const apiUrl = "http://localhost:5003";

export const useAppointmentStore = defineStore("appointment", {
  state: () => ({
    appointments: [
      {
        id: null,
        patientId: null,
        doctorId: null,
        date: null,
        time: null,
        patientName: "",
        doctorName: "",
        createdAt: "",
        status: "",
      },
    ],
    approvedAppointments: 0,
    pendingAppointments: 0,
    rejectedAppointments: 0,
  }),

  actions: {
    async createAppointment(data) {
      try {
        data.date = new Date(data.date).toISOString();
        const res = await axios.post(`${apiUrl}/create-appointment`, data, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 201) {
          await router.push("/appointments");
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          await this.createAppointment(data);
        }
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
        } else {
          this.appointments = [];
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          window.location.reload();
        }
        console.error("Error getting appointments: ", error);
        throw error;
      }
    },

    async approveAppointment(appointmentId) {
      try {
        const res = await axios.put(
          `${apiUrl}/appointment/approve/${appointmentId}`,
          appointmentId,
          {
            headers: {
              Authorization: "Bearer " + useAuthStore().auth.accessToken,
            },
          },
        );
        if (res.status === 200) {
          await this.getAppointments();
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          await this.approveAppointment(appointmentId);
        }
        console.error("Error setting appointment status: ", error);
        throw error;
      }
    },

    async rejectAppointment(appointmentId) {
      try {
        const res = await axios.put(
          `${apiUrl}/appointment/reject/${appointmentId}`,
          appointmentId,
          {
            headers: {
              Authorization: "Bearer " + useAuthStore().auth.accessToken,
            },
          },
        );
        if (res.status === 200) {
          await this.getAppointments();
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          await this.rejectAppointment(appointmentId);
        }
        console.error("Error setting appointment status: ", error);
        throw error;
      }
    },

    async cancelAppointment(appointmentId) {
      try {
        const res = await axios.put(
          `${apiUrl}/appointment/cancel/${appointmentId}`,
          appointmentId,
          {
            headers: {
              Authorization: "Bearer " + useAuthStore().auth.accessToken,
            },
          },
        );
        if (res.status === 200) {
          await this.getAppointments();
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          await this.cancelAppointment(appointmentId);
        }
        console.error("Error setting appointment status: ", error);
        throw error;
      }
    },

    async restoreAppointment(appointmentId) {
      try {
        const res = await axios.put(
          `${apiUrl}/appointment/restore/${appointmentId}`,
          appointmentId,
          {
            headers: {
              Authorization: "Bearer " + useAuthStore().auth.accessToken,
            },
          },
        );
        if (res.status === 200) {
          await this.getAppointments();
        }
      } catch (error) {
        if (error.response.status === 401) {
          await useAuthStore().refreshAccessToken();
          await this.restoreAppointment(appointmentId);
        }
        console.error("Error setting appointment status: ", error);
        throw error;
      }
    },

    async countApprovedAppointments() {
      try {
        const res = await axios.get(`${apiUrl}/appointment/count-approved`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        this.approvedAppointments = res.data;
      } catch (error) {
        console.error("Error counting approved appointments: ", error);
        throw error;
      }
    },

    async countPendingAppointments() {
      try {
        const res = await axios.get(`${apiUrl}/appointment/count-pending`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        this.pendingAppointments = res.data;
      } catch (error) {
        console.error("Error counting pending appointments: ", error);
        throw error;
      }
    },

    async countRejectedAppointments() {
      try {
        const res = await axios.get(`${apiUrl}/appointment/count-rejected`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        this.rejectedAppointments = res.data;
      } catch (error) {
        console.error("Error counting rejected appointments: ", error);
        throw error;
      }
    },
    
    async getApprovedAppointments() {
      try {
        await this.getAppointments();
        this.appointments = this.appointments.filter(
          (appointment) => appointment.status === "odobren",
        );
      } catch (error) {
        console.error("Error getting patient's approved appointments: ", error);
        throw error;
      }
    }
  },
});
