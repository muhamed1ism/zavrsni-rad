import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import { useAuthStore } from "@/stores/useAuthStore";
import axios from "axios";
import router from "@/router";

const apiUrl = "http://localhost:5000";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: useLocalStorage("user", {
      id: null,
      email: "",
      role: "",
      createdAt: "",
      updatedAt: "",
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

    async getUser() {
      const getUserApiCall = () =>
        axios.get(`${apiUrl}/get-user`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
      const res = await this.makeApiRequest(
        getUserApiCall,
        "Error getting user data",
      );

      if (res.status === 200) {
        this.user = {
          id: res.data.id,
          email: res.data.email,
          role: res.data.role,
          createdAt: res.data.createdAt,
          updatedAt: res.data.updatedAt,
        };
      }
    },

    async clearUser() {
      try {
        this.user = {
          id: null,
          email: "",
          role: "",
          createdAt: "",
          updatedAt: "",
        };
      } catch (error) {
        console.error("Error: ", error);
        throw error;
      }
    },

    async updateEmail(email) {
      const updateEmailApiCall = () =>
        axios.put(`${apiUrl}/update-email`, email, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
      const res = await this.makeApiRequest(
        updateEmailApiCall,
        "Error updating email",
      );

      if (res.status === 200) {
        this.user.email = email;
        await router.push("/settings");
      }
    },

    async updatePassword(passwords) {
      const updatePasswordApiCall = () =>
        axios.put(`${apiUrl}/update-password`, passwords, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
      const res = await this.makeApiRequest(
        updatePasswordApiCall,
        "Error updating password",
      );

      if (res.status === 200) {
        await router.push("/settings");
      }
    },
  },
});
