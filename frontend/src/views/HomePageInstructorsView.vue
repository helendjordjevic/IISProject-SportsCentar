<template>
  <div class="home-view">
    <h1>My Trainings 🏋️‍♂️</h1>

    <div v-if="trainings.length" class="trainings-container">
      <div
        v-for="training in trainings"
        :key="training.training_id"
        class="training-card"
        @click="goToTraining(training.training_id)"
      >
        <p><strong>Name:</strong> {{ training.name }}</p>
        <p><strong>Type:</strong> {{ training.training_type || '—' }}</p>
      </div>
    </div>

    <div v-else>
      <p>You don't have any trainings assigned yet.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      trainings: []
    };
  },
  methods: {
    async fetchTrainings(instructorId) {
      try {
        const url = `http://localhost:8000/trainings/instructor/${instructorId}`;
        const response = await axios.get(url);
        this.trainings = response.data;
        console.log("Fetched trainings for instructor:", this.trainings);
      } catch (error) {
        console.error("Error fetching trainings:", error.response?.data || error.message);
      }
    },
    goToTraining(trainingId) {
      this.$router.push({ path: `/training/${trainingId}` });
    }
  },
  created() {
    const instructorId = localStorage.getItem("userId");
    if (instructorId) {
      this.fetchTrainings(instructorId);
    } else {
      console.error("Instructor ID not found in localStorage");
    }
  }
};
</script>

<style>
.home-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background-color: #F0F6F6;
}

h1 {
  color: rgb(0, 100, 180);
  margin-bottom: 30px;
}

.trainings-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 90%;
  max-width: 900px;
}

.training-card {
  padding: 20px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.training-card:hover {
  transform: scale(1.02);
}
</style>
