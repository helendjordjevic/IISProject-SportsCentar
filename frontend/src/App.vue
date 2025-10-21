<template>
  <nav class="navbar navbar-expand-lg" style="background-color: rgb(0, 175, 240);">
   <div class="container-fluid">
      <router-link class="brand" to="/">🏋️ Sports Center</router-link>

      <div 
        v-if="!isTrainingDetailsPage" 
        class="search-section"
      >
        <input 
          type="text" 
          placeholder="Search trainings..." 
          v-model="searchText"
          @keyup.enter="searchTrainings"
          class="search-input"
        />

        <select v-model="searchFilter" class="filter-select">
          <option value="name">Name</option>
          <option value="type">Type</option>
        </select>

        <button type="button" class="search-btn" @click="searchTrainings">
          <font-awesome-icon icon="magnifying-glass" />
        </button>
      </div>

      <div class="auth-section">
        <template v-if="!isLoggedIn">
          <router-link class="nav-btn" to="/login">Login</router-link>
          <router-link class="nav-btn" to="/register">Register</router-link>
        </template>

        <template v-else>
          <router-link v-if="isClient" class="nav-btn" to="/profile">My Profile</router-link>
          <router-link v-if="isAdmin" class="nav-btn" to="/weekly-report">Weekly Report</router-link>
          <router-link v-if="isInstructor" class="nav-btn" to="/instructor-dashboard">Instructor Dashboard</router-link>
          <button class="nav-btn" @click="logout">Logout</button>
        </template>
      </div>

    </div>
  </nav>

  <router-view :searchQuery="searchText" :searchFilter="searchFilter"/>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchText: '',
      searchFilter: 'name',
      isLoggedIn: !!localStorage.getItem('userEmail') // reactive check
    };
  },
  computed: 
  {
    isTrainingDetailsPage() {
      return this.$route.name === 'trainingDetail';
    }, isClient() {
    return localStorage.getItem("userType") === "CLIENT";
  },
  isAdmin() {
    return localStorage.getItem("userType") === "ADMIN";
  },
  isInstructor() {
    return localStorage.getItem("userType") === "INSTRUCTOR";
  }
},
  watch: {
    // kad se ruta promeni, proveri da li je korisnik logovan
    '$route'() {
      this.isLoggedIn = !!localStorage.getItem('userEmail');
    }
  },
  methods: {
    logout() {
      localStorage.removeItem("userEmail");
      localStorage.removeItem("userId");
      localStorage.removeItem("userType");
      this.isLoggedIn = false;
      this.$router.push("/login");
    },
    searchTrainings() {
      console.log("Searching for:", this.searchText, "with filter:", this.searchFilter);
    }
  },
  created() {
    // Axios interceptor za slanje tokena
    axios.interceptors.request.use(config => {
      const token = localStorage.getItem("token");
      if (token) config.headers.Authorization = `Bearer ${token}`;
      return config;
    });
  }
};
</script>

<style scoped>
.custom-navbar {
  background: linear-gradient(90deg, rgb(0, 160, 230), rgb(0, 200, 255));
  padding: 12px 30px;
  display: flex;
  align-items: center;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

.brand {
  color: white;
  font-weight: 700;
  font-size: 22px;
  text-decoration: none; 
  margin-right: auto;
}

.brand:hover {
  color: #dff6ff;
}

/* Search bar + filter */
.search-section {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 25px;
  padding: 4px 10px;
  width: 420px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 8px 12px;
  border-radius: 20px;
  font-size: 15px;
}

.filter-select {
  border: none;
  outline: none;
  background: transparent;
  color: #0078c2;
  font-weight: 600;
  margin-left: 8px;
}

.search-btn {
  background: transparent;
  border: none;
  color: #0078c2;
  cursor: pointer;
  font-size: 18px;
  margin-left: 8px;
}

/* Login / Register sekcija */
.auth-section {
  display: flex;
  gap: 12px;
  align-items: center;
}

.nav-btn {
  text-decoration: none; 
  color: white;
  background-color: #0078c8; 
  border: 2px solid white;
  padding: 6px 14px;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 3px 6px rgba(255,255,255,0.3);
}

.nav-btn:hover {
  background-color: white;
  color: #0078c8;
  border-color: #0078c8;
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0,0,0,0.25);
}
</style>