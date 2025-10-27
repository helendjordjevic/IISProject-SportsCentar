<template>
  <div class="container mt-4">
    <h2>Your Recommended Trainings</h2>

    <div class="mb-3">
      <label for="topN" class="form-label">Number of recommendations:</label>
      <input
        type="number"
        id="topN"
        v-model.number="topN"
        class="form-control"
        min="1"
        max="20"
      />
      <button class="btn btn-primary mt-2" @click="fetchRecommendations">Load</button>
    </div>

    <div v-if="loading" class="text-center my-4">Loading...</div>

    <div v-else>
      <table class="table table-striped" v-if="recommendations.length">
        <thead>
          <tr>
            <th>Traning</th>
            <th>Type</th>
            <th>Instructor</th>
            <th>Difficulty</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in recommendations" :key="t.training_id">
            <td>{{ t.training_name }}</td>
            <td>{{ t.training_type }}</td>
            <td>{{ t.instructor_name }}</td>
            <td>{{ t.difficulty_level }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No recommendations available.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      recommendations: [],
      loading: false,
      topN: 5,
      clientId: localStorage.getItem("userId") 
    };
  },
  methods: {
    fetchRecommendations() {
      if (!this.clientId) return;

      this.loading = true;

      axios.get(`http://127.0.0.1:8000/recommendations/${this.clientId}`, {
        params: { top_n: this.topN }
      })
      .then(res => {
        this.recommendations = res.data || [];
      })
      .catch(err => {
        console.error("Error fetching recommendations:", err);
        alert("Failed to load recommendations");
      })
      .finally(() => {
        this.loading = false;
      });
    }
  },
  mounted() {
    this.fetchRecommendations(); 
  }
};
</script>

<style scoped>
h2 {
  color: #0078c8;
}
</style>
