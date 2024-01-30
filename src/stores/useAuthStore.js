import { defineStore } from "pinia";
import { useUserStore } from "@/stores/useUserStore";
import { usePatientStore } from "@/stores/usePatientStore";

const apiUrl = "http://localhost:5000";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access_token: "",
    refresh_token: "",
  }),

  actions: {
    async register(email, password, password_confirm, role) {
      const res = await fetch(`${apiUrl}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
          password_confirm,
          role,
        }),
      });

      const data = await res.json();
      if (data.error) {
        throw data.error;
      }

      this.access_token = data.access_token;
      this.refresh_token = data.refresh_token;

      localStorage.setItem("access_token", this.access_token);
      localStorage.setItem("refresh_token", this.refresh_token);

      await this.login(email, password);
    },

    async login(email, password) {
      const res = await fetch(`${apiUrl}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await res.json();
      if (data.error) {
        throw data.error;
      }

      this.access_token = data.access_token;
      this.refresh_token = data.refresh_token;

      localStorage.setItem("access_token", this.access_token);
      localStorage.setItem("refresh_token", this.refresh_token);

      const userStore = useUserStore();
      await userStore.getUser();

      window.location.href = "/dashboard";
    },

    async logout() {
      await fetch(`${apiUrl}/logout`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      });

      await fetch(`${apiUrl}/logout`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("refresh_token"),
        },
      });

      this.access_token = "";
      this.refresh_token = "";

      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      const userStore = useUserStore();
      await userStore.clearUser();
      const patientStore = usePatientStore();
      await patientStore.clearPatient();

      window.location.href = "/";
    },
  },

  getters: {
    isAuthenticated: () => {
      return localStorage.getItem("access_token") !== null;
    },
  },
});
