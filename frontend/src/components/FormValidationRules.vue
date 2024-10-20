<script>
  export const rules = {
    firstName: [
      (v) => !!v || "First name is required",
      (v) => (v && v.length <= 20) || "First name must be less than 20 characters",
    ],

    lastName: [
      (v) => !!v || "Last name is required",
      (v) => (v && v.length <= 20) || "Last name must be less than 20 characters",
    ],

    specialty: [
      (v) => !!v || "Specialty is required",
      (v) => (v && v.length <= 20) || "Specialty must be less than 20 characters",
    ],

    phoneNumber: [
      (v) => {
        const numberWithoutSpace = v.replace(/\s+/g, "");
        const regex = /^[0-9+]+$/;
        if (!regex.test(numberWithoutSpace) && numberWithoutSpace !== "") {
          return "Phone number must contain only numbers";
        }
        return true;
      },
    ],

    email: [
      (v) => !!v || "Email is required",
      (v) => /.+@.+/.test(v) || "Email must be valid",
    ],

    currentPassword: [(v) => !!v || "Current password is required"],

    password: [
      (v) => !!v || "Password is required",
      (v) => (v && v.length >= 8) || "Password must be at least 8 characters",
    ],

    passwordConfirm: (password) => [
      (v) => !!v || "Password confirmation is required",
      (v) => v === password || "Passwords do not match",
    ],

    role: [(v) => !!v || "Role is required"],
  };
</script>

<template>

</template>

<style scoped>

</style>