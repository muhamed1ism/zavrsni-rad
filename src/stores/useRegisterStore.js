import { defineStore } from "pinia";
import {useAuthStore} from "@/stores/useAuthStore";
import {usePatientStore} from "@/stores/usePatientStore";
import {useDoctorStore} from "@/stores/useDoctorStore";

export const useRegisterStore = defineStore("register", {
  state: () => ({
    register: {
        user: {
            email: "",
            password: "",
            confirm_password: "",
            role: "patient",
        },
        profile: {
            first_name: "",
            last_name: "",
            date_of_birth: "",
            phone_number: "",
            address: "",
        }
    },
  }),
  actions: {
    setRegisterUser(user) {
      this.register.user = user;
    },

    setRegisterProfile(profile) {
      this.register.profile = profile;
    },

      async registerUser(data) {
        this.setRegisterUser(data.user);
        this.setRegisterProfile(data.profile);
        const res = await useAuthStore().register(this.register.user);
        if (res.status === 201) {
          if (this.register.user.role === "patient") {
            await usePatientStore().createPatient(this.register.profile);
          } else {
            await useDoctorStore().createDoctor(this.register.profile);
          }
          window.location.href = "/dashboard";
        }
      }

  },
});
