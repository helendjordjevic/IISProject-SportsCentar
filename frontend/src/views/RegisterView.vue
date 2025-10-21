<template>
  <div class="wrapper">
    <form class="kanta" @submit.prevent="registerUser">
      <div v-if="error" class="alert alert-danger mx-2">
        {{ error }}
      </div>

      <div class="form-group">
        <label>First Name</label>
        <input type="text" class="form-control" v-model="registerDto.first_name" required />
      </div>

      <div class="form-group">
        <label>Last Name</label>
        <input type="text" class="form-control" v-model="registerDto.last_name" required />
      </div>

      <div class="form-group">
        <label>Email</label>
        <input type="email" class="form-control" v-model="registerDto.email" required />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input type="password" class="form-control" v-model="registerDto.password" required />
      </div>

      <input type="hidden" v-model="registerDto.user_type" />

      <button id="submit-button">Register</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "RegisterView",
  data() {
    return {
      registerDto: {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        user_type: "CLIENT" 
      },
      error: ""
    };
  },
  methods: {
    async registerUser() {
        if (!this.registerDto.email.includes("@")) {
        this.error = "Email mora sadržati znak '@'.";
        return;
      } else {
        this.error = "";
      }
      try {
        const response = await axios.post("http://localhost:8000/users", this.registerDto);
        const user = response.data;

        localStorage.setItem("userEmail", user.email);
        localStorage.setItem("userId", user.user_id);
        localStorage.setItem("userType", user.user_type);

        await Swal.fire({
          title: "Uspešna registracija!",
          text: `Dobrodošli, ${user.first_name}!`,
          icon: "success",
          confirmButtonColor: "rgb(0, 175, 240)"
        });

        this.$router.push({ name: "home" });

      } catch (error) {
        console.error(error);
        if (error.response && error.response.status === 409) {
          this.error = "Korisnik sa ovim emailom već postoji.";
        } else {
          this.error = "Došlo je do greške prilikom registracije.";
        }
      }
    }
  }
};
</script>

<style>
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f6f6;
}

.kanta {
  width: 400px;
  padding: 40px 30px;
  border-radius: 15px;
  background-color: #ffffff;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.form-group { margin-bottom: 20px; width: 100%; }

label { font-weight: bold; display: block; margin-bottom: 5px; color: rgb(0, 90, 150); }

.form-control {
  width: 100%; height: 45px; border-radius: 25px; border: 1px solid #ccc; padding: 10px 15px; font-size: 16px;
  transition: 0.3s;
}

.form-control:focus {
  border-color: rgb(0, 175, 240);
  box-shadow: 0 0 5px rgba(0, 175, 240, 0.3);
  outline: none;
}

#submit-button {
  width: 100%; height: 45px; background-color: rgb(0, 175, 240); color: white; border: none; border-radius: 25px;
  font-size: 18px; font-weight: bold; cursor: pointer; transition: 0.3s;
}

#submit-button:hover { background-color: rgb(0, 145, 220); }

.alert {
  color: red;
  margin-bottom: 10px;
  font-weight: bold;
  text-align: center;
}
</style>
