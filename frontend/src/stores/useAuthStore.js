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
      refreshTokenTimer: null,
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
          await this.startRefreshTokenTimer();
        }
      } catch (error) {
        console.error("Login error: ", error);
        throw error;
      }
    },

    async startRefreshTokenTimer() {
      try {
        const jwtToken = JSON.parse(atob(this.auth.accessToken.split(".")[1]));
        const expires = new Date(jwtToken.exp * 1000);
        const timeout = expires - Date.now() - 60 * 1000;
        this.auth.refreshTokenTimer = setTimeout(
          this.refreshAccessToken,
          timeout,
        );
      } catch (error) {
        console.error("Refresh token timer error: ", error);
        throw error;
      }
    },

    async stopRefreshTokenTimer() {
      clearTimeout(this.auth.refreshTokenTimer);
      this.auth.refreshTokenTimer = null;
    },

    async refreshAccessToken() {
      try {
        const res = await axios.post(
          `${apiUrl}/refresh-token`,
          this.auth.refreshToken,
        );
        if (res.status === 200) {
          this.auth.accessToken = res.data.accessToken;
        }
      } catch (error) {
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
        await this.revokeAccessToken();
        await this.revokeRefreshToken();
        await this.clearUserData();
        await this.stopRefreshTokenTimer();
        this.auth.hasProfile = false;
        this.auth.isAuthenticated = false;
    },
  },
});
