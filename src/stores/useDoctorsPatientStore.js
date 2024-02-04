import {defineStore} from "pinia";
import axios from "axios";
import {useAuthStore} from "@/stores/useAuthStore";

const apiUrl = "http://localhost:5003";

export const useDoctorsPatientStore = defineStore("patient", {
    state: () => ({
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

        async getPatients() {
            const getPatientsApiCall = () =>
                axios.get(`${apiUrl}/get-doctors-patients`, {
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
        }
    }
});