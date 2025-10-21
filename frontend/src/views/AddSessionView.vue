<template>
  <div class="add-session-view">
    <h1>Add New Session for {{ training.name }}</h1>

    <form @submit.prevent="createSession" class="session-form">
      <!-- Instruktor -->
      <label for="instructor">Instructor:</label>
      <select v-model="form.instructor_id" required>
        <option disabled value="">Select instructor</option>
        <option v-for="instr in instructors" :key="instr.user_id" :value="instr.user_id">
          {{ instr.first_name }} {{ instr.last_name }}
        </option>
      </select>

      <!-- Studio -->
      <label for="studio">Studio:</label>
      <select v-model="form.training_studio_id" required>
        <option disabled value="">Select studio</option>
        <option v-for="studio in studios" :key="studio.training_studio_id" :value="studio.training_studio_id">
            {{ studio.training_studio_number }}
        </option>
      </select>

      <!-- Start Time -->
      <label for="start_time">Start Time:</label>
      <input type="datetime-local" v-model="form.start_time" required />

      <!-- End Time -->
      <label for="end_time">End Time:</label>
      <input type="datetime-local" v-model="form.end_time" required />

      <button type="submit">Create Session</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      training: {},
      instructors: [],
      studios: [],
      form: {
        instructor_id: "",
        training_studio_id: "",
        start_time: "",
        end_time: ""
      }
    };
  },
  methods: {
    async fetchTraining() {
      const trainingId = this.$route.params.trainingId;
      try {
        const res = await axios.get(`http://localhost:8000/trainings/${trainingId}`);
        this.training = res.data;
      } catch (error) {
        console.error("Error fetching training:", error);
      }
    },
    async fetchInstructors() {
      try {
        const res = await axios.get("http://localhost:8000/users/all/instructors");
        this.instructors = res.data;
      } catch (error) {
        console.error("Error fetching instructors:", error);
      }
    },
    async fetchStudios() {
      try {
        const res = await axios.get("http://localhost:8000/studios/");
        this.studios = res.data;
      } catch (error) {
        console.error("Error fetching studios:", error);
      }
    },
    async createSession() {
        const trainingId = this.$route.params.trainingId; // ovo je ključ
        try {
            const payload = {
            start_time: this.form.start_time,
            end_time: this.form.end_time,
            training_id: parseInt(trainingId), // obavezno int
            training_studio_id: this.form.training_studio_id,
            instructor_id: this.form.instructor_id
            };

            await axios.post("http://localhost:8000/sessions/", payload);

            await Swal.fire({
            title: "Success",
            text: "Session created successfully!",
            icon: "success",
            confirmButtonColor: "rgb(0, 175, 240)"
            });

            this.$router.push(`/training/${trainingId}`);
        } catch (error) {
            console.error("Error creating session:", error);
            let message = "Došlo je do greške prilikom kreiranja termina.";
            if (error.response && error.response.data) {
            if (typeof error.response.data === "string") {
                message = error.response.data;
            } else if (error.response.data.message) {
                message = error.response.data.message;
            } else {
                message = JSON.stringify(error.response.data);
            }
            }
            await Swal.fire({
            title: "Error",
            text: message,
            icon: "error",
            confirmButtonColor: "rgb(0, 175, 240)"
            });
        }
        }

  },
  created() {
    this.fetchTraining();
    this.fetchInstructors();
    this.fetchStudios();
  }
};
</script>

<style>
.add-session-view {
  padding: 40px;
  background-color: #F0F6F6;
  min-height: 100vh;
}

h1 {
  color: rgb(0, 100, 180);
  margin-bottom: 20px;
}

.session-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 500px;
}

label {
  font-weight: 600;
  color: #333;
}

input, select {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: rgb(0, 175, 240);
  border: none;
  border-radius: 20px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: rgb(0, 145, 220);
}
</style>
