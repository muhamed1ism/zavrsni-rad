import {defineStore} from "pinia";
import axios from "axios";
import {useAuthStore} from "@/stores/useAuthStore";

const apiUrl = "http://localhost:5003";

export const useDoctorsPatientStore = defineStore("patient", {
    state: () => ({
        patients: [],
    }),

    actions: {
        async getPatients() {
            try {
                const res = await axios.get(`${apiUrl}/get-doctors-patients`, {
                    headers: {
                        Authorization: "Bearer " + useAuthStore().auth.accessToken,
                    },
                });
                if (res.status === 200) {
                    this.patients = res.data;
                }
            } catch (error) {
                console.error("Error getting patients: ", error);
                throw error;
            }
        }
    }
});