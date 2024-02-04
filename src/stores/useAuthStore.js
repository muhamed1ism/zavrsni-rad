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
    async makeApiRequest(callback, errorMessage) {
      try {
        return await callback();
      } catch (error) {
        console.error(`${errorMessage}: `, error);
        throw error;
      }
    },

    async register(credentials) {
      const registerApiCall = () =>
        axios.post(`${apiUrl}/register`, credentials);
      const res = await this.makeApiRequest(
        registerApiCall,
        "Registration error",
      );

      if (res.status === 201) {
        await this.login({
          email: credentials.email,
          password: credentials.password,
        });
      }
    },

    async login(credentials) {
      const loginApiCall = () => axios.post(`${apiUrl}/login`, credentials);
      const res = await this.makeApiRequest(loginApiCall, "Login error");

      if (res.status === 200) {
        this.auth = {
          isAuthenticated: true,
          accessToken: res.data.accessToken,
          refreshToken: res.data.refreshToken,
        };
      }
    },

    async refreshAccessToken() {
      const refreshApiCall = () =>
        axios.post(`${apiUrl}/refresh-token`, this.auth.refreshToken);
      const res = await this.makeApiRequest(
        refreshApiCall,
        "Refresh token error",
      );

      if (res.status === 200) {
        this.auth.accessToken = res.data.accessToken;
      }
    },

    async revokeAccessToken() {
      const deleteAuthApiCall = () =>
        axios.delete(`${apiUrl}/logout`, {
          headers: {
            Authorization: `Bearer ${this.auth.accessToken}`,
          },
        });
      const res = await this.makeApiRequest(
        deleteAuthApiCall,
        "Error revoking access token",
      );

      if (res.status === 401) {
        await this.refreshAccessToken();
        await this.revokeAccessToken();
      }
      if (res.status === 200) {
        this.auth.accessToken = "";
      }
    },

    async revokeRefreshToken() {
      const deleteAuthApiCall = () =>
        axios.delete(`${apiUrl}/logout`, {
          headers: {
            Authorization: `Bearer ${this.auth.refreshToken}`,
          },
        });
      const res = await this.makeApiRequest(
        deleteAuthApiCall,
        "Error revoking refresh token",
      );

      if (res.status === 200) {
        this.auth.refreshToken = "";
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
        this.auth.hasProfile = false;
        this.auth.isAuthenticated = false;
      } catch (error) {
        console.error("Logout error: ", error);
        throw error;
      }
    },
  },
});
