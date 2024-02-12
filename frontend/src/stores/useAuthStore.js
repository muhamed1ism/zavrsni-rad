import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import { useUserStore } from "@/stores/useUserStore";
import { usePatientStore } from "@/stores/usePatientStore";
import { useDoctorStore } from "@/stores/useDoctorStore";
import axios from "axios";

const apiUrl = "http://localhost:5000";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    auth: useLocalStorage("auth", {
      hasProfile: false,
      isAuthenticated: false,
      accessToken: "",
      refreshToken: "",
    }),
  }),

  actions: {
    async register(credentials) {
      try {
        const res = await axios.post(`${apiUrl}/register`, credentials);
        if (res.status === 201) {
          await this.login({
            email: credentials.email,
            password: credentials.password,
          });
        }
      } catch (error) {
        console.error("Register error: ", error);
        throw error;
      }
    },

    async login(credentials) {
      try {
        const res = await axios.post(`${apiUrl}/login`, credentials);
        if (res.status === 200) {
          this.auth = {
            isAuthenticated: true,
            accessToken: res.data.accessToken,
            refreshToken: res.data.refreshToken,
          };
        }
      } catch (error) {
        console.error("Login error: ", error);
        throw error;
      }
    },

    async refreshAccessToken() {
      try {
        const res = await axios.post(`${apiUrl}/refresh-token`, null,{
          headers: {
            Authorization: `Bearer ${this.auth.refreshToken}`,
          }
        });
        if (res.status === 200) {
          this.auth.accessToken = res.data.accessToken;
        }
      } catch (error) {
        if (error.response.status === 401) {
          await this.clearUserData();
          this.auth.hasProfile = false;
          this.auth.isAuthenticated = false;
          window.location.href = "/login";
        }
        console.error("Refresh access token error: ", error);
        throw error;
      }
    },

    async revokeAccessToken() {
      try {
        const res = await axios.delete(`${apiUrl}/logout`, {
          headers: {
            Authorization: `Bearer ${this.auth.accessToken}`,
          },
        });
        if (res.status === 200) {
          this.auth.accessToken = "";
        }
      } catch (error) {
        console.error("Revoke access token error: ", error);
        throw error;
      }
    },

    async revokeRefreshToken() {
      try {
        const res = await axios.delete(`${apiUrl}/logout`, {
          headers: {
            Authorization: `Bearer ${this.auth.refreshToken}`,
          },
        });

        if (res.status === 200) {
          this.auth.refreshToken = "";
        }
      } catch (error) {
        console.error("Revoke refresh token error: ", error);
        throw error;
      }
    },

    async clearUserData() {
      const role = useUserStore().user.role;
      if (role === "patient") {
        await usePatientStore().clearPatient();
      } else if (role === "doctor") {
        await useDoctorStore().clearDoctor();
      }
      await useUserStore().clearUser();
    },

    async logout() {
      try {
        await this.revokeAccessToken();
        await this.revokeRefreshToken();
        await this.clearUserData();
        this.auth.hasProfile = false;
        this.auth.isAuthenticated = false;
      } catch (error) {
        if (error.response.status === 401) {
          await this.refreshAccessToken();
          await this.logout();
          window.location.href = "/login";
        }
        console.error("Logout error: ", error);
        throw error;
      }

    },
  },
});
