<script>
  export const rules = {
    firstName: [
      (v) => !!v || "Ime je obavezno",
      (v) => (v && v.length <= 20) || "Ime mora biti manje od 20 karaktera",
    ],

    lastName: [
      (v) => !!v || "Prezime je obavezno",
      (v) => (v && v.length <= 20) || "Prezime mora biti manje od 20 karaktera",
    ],

    specialty: [
      (v) => !!v || "Specijalnost je obavezna",
      (v) => (v && v.length <= 20) || "Specijalnost mora biti manje od 20 karaktera",
    ],

    phoneNumber: [
      (v) => {
        const numberWithoutSpace = v.replace(/\s+/g, "");
        const regex = /^[0-9+]+$/;
        if (!regex.test(numberWithoutSpace) && numberWithoutSpace !== "") {
          return "Broj telefona nije validan. Dozvoljeni su samo brojevi i znak +";
        }
        return true;
      },
    ],

    email: [
      (v) => !!v || "Email je obavezan",
      (v) => /.+@.+/.test(v) || "Email nije validan",
    ],

    currentPassword: [(v) => !!v || "Trenutna lozinka je obavezna"],

    password: [
      (v) => !!v || "Lozinka je obavezna",
      (v) => (v && v.length >= 8) || "Lozinka mora biti duža od 8 karaktera",
    ],

    passwordConfirm: (password) => [
      (v) => !!v || "Potvrda lozinke je obavezna",
      (v) => v === password || "Lozinke se ne poklapaju",
    ],

    role: [(v) => !!v || "Role je obavezan"],
  };
</script>

<template>

</template>

<style scoped>

</style>