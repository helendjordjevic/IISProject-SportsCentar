<template>
  <div class="home-view">
    <h1>Trainings</h1>
    <div class="trainings-container">
      <div v-for="training in trainings" :key="training.training_id" class="training-card" @click="goToTraining(training.training_id)">
      <p><strong>Name:</strong> {{ training.name }}</p>
      <p><strong>Type:</strong> {{ training.training_type }}</p>
      <p>{{ training.description }}</p>
    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: ['searchQuery', 'searchFilter'],
  data() {
    return {
      trainings: []
    };
  },
  watch: {
    searchQuery(newQuery) {
      this.fetchTrainings(newQuery, this.searchFilter);
    },
    searchFilter(newFilter) {
      this.fetchTrainings(this.searchQuery, newFilter);
    }
  },
  methods: {
    async fetchTrainings(query = '', filter = 'name') {
      try {
        let url = 'http://localhost:8000/trainings';
        if (query && query.trim() !== '') {
          if (filter === 'name') {
            url = `http://localhost:8000/trainings/search/name/${query}`;
          } else if (filter === 'type') {
            url = `http://localhost:8000/trainings/search/type/${query}`;
          }
        }

        const response = await axios.get(url);
        this.trainings = response.data;
        console.log('Trainings fetched:', this.trainings);
      } catch (error) {
        console.error(' Error fetching trainings:', error.response?.data || error.message);
      }
    },
    goToTraining(trainingId) {
      this.$router.push({ path: `/training/${trainingId}` });
    }
  },
  created() {
    this.fetchTrainings();
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

.training-card h3 {
  margin: 0 0 10px 0;
  color: rgb(0, 100, 180);
}

.training-card p {
  margin: 0;
  color: #333;
}
</style>
