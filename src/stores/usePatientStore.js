import { defineStore } from "pinia";

const apiUrl = "http://localhost:5001";

export const usePatientStore = defineStore("patient", {
  state: () => ({
    patient: {
      id: "",
      first_name: "",
      last_name: "",
      date_of_birth: "",
      address: "",
      phone_number: "",
    }
  }),

  actions: {
    async createPatient(
      first_name,
      last_name,
      date_of_birth,
      address,
      phone_number,
    ) {
      try {
        const res = await fetch(`${apiUrl}/create-patient`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            first_name,
            last_name,
            date_of_birth,
            address,
            phone_number,
          }),
        });

        const data = await res.json();
        if (data.error) {
          console.log(data.error);
        }

        await this.getPatient();

        window.location.href = "/dashboard";
      } catch (error) {
        console.error("Failed to create patient: " + error);
        throw error;
      }
    },

    async getPatient() {
      try {
        const res = await fetch(`${apiUrl}/get-patient`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        });

        const data = await res.json();
        if (data.error) {
          console.log(data.error);
        }

        this.patient = data;
        if (this.patient) {
          await this.setPatient();
        }
      } catch (error) {
        console.error("Failed to get patient: " + error);
        throw error;
      }
    },

    async setPatient() {
      localStorage.setItem("patient_id", this.patient.id);
      localStorage.setItem("first_name", this.patient.first_name);
      localStorage.setItem("last_name", this.patient.last_name);
      localStorage.setItem("date_of_birth", this.patient.date_of_birth);
      localStorage.setItem("address", this.patient.address);
      localStorage.setItem("phone_number", this.patient.phone_number);
    },

    async clearPatient() {
      localStorage.removeItem("patient_id");
      localStorage.removeItem("first_name");
      localStorage.removeItem("last_name");
      localStorage.removeItem("date_of_birth");
      localStorage.removeItem("address");
      localStorage.removeItem("phone_number");
    },

    async updatePatient(
      first_name,
      last_name,
      date_of_birth,
      address,
      phone_number,
    ) {
      try {
        await fetch(`${apiUrl}/update-patient`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            first_name,
            last_name,
            date_of_birth,
            address,
            phone_number,
          }),
        });
      } catch (error) {
        console.error("Failed to update patient: " + error);
        throw error;
      }
    },
  },
});
