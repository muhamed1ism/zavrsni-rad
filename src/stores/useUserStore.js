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
    async getUser() {
      try {
        const res = await axios.get(`${apiUrl}/get-user`, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 200) {
          this.user = {
            id: res.data.id,
            email: res.data.email,
            role: res.data.role,
            createdAt: res.data.createdAt,
            updatedAt: res.data.updatedAt,
          };
        }
      } catch (error) {
        console.error("Error getting user data: ", error);
        throw error;
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
      try {
        const res = await axios.put(
          `${apiUrl}/update-email`,
          { email: email },
          {
            headers: {
              Authorization: "Bearer " + useAuthStore().auth.accessToken,
            },
          },
        );
        if (res.status === 200) {
          this.user.email = email;
          await router.push("/settings");
        }
      } catch (error) {
        console.error("Error updating email: ", error);
        throw error;
      }
    },

    async updatePassword(passwords) {
      try {
        const res = await axios.put(`${apiUrl}/update-password`, passwords, {
          headers: {
            Authorization: "Bearer " + useAuthStore().auth.accessToken,
          },
        });
        if (res.status === 200) {
          await router.push("/settings");
        }
      } catch (error) {
        console.error("Error updating password: ", error);
        throw error;
      }
    },
  },
});
