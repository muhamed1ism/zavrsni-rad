import { defineStore } from "pinia";

const apiUrl = "http://localhost:5000"

export const useUserStore = defineStore("user", {
    state: () => ({
        user: {
            id: "",
            email: "",
            role: "",
            created_at: "",
            updated_at: "",
        }
    }),

    actions: {
        async getUser() {
                const res = await fetch(`${apiUrl}/get-user`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("access_token"),
                    },
                });

                const data = await res.json();
                if (data.error) {
                    throw ("Failed to get user: " + data.error);
                }

                this.user = data;
                if (this.user) {
                    await this.setUser();
                }
        },

        async setUser() {
                localStorage.setItem("id", this.user.id);
                localStorage.setItem("email", this.user.email);
                localStorage.setItem("role", this.user.role);
                localStorage.setItem("createdAt", this.user.created_at);
                localStorage.setItem("updatedAt", this.user.updated_at);
        },

        async clearUser() {
                localStorage.removeItem("id");
                localStorage.removeItem("email");
                localStorage.removeItem("role");
                localStorage.removeItem("createdAt");
                localStorage.removeItem("updatedAt");
        },

        async updateEmail(email) {
                const res = await fetch(`${apiUrl}/update-email`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("access_token")
                    },
                    body: JSON.stringify({
                        email,
                    }),
                });

                const data = await res.json();
                this.email = data.email;

                localStorage.setItem("email", this.email);
        },

        async updatePassword(current_password, new_password, new_password_confirm) {
                await fetch(`${apiUrl}/update-password`,{
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("access_token")
                    },
                    body: JSON.stringify({
                        current_password,
                        new_password,
                        new_password_confirm,
                    }),
                });
        },

    },
})