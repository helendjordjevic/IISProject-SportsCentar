<template>
  <div class="profile-view">
    <h1></h1>

    
   <div v-if="!userId">
      <p>You need to log in to see your profile.</p>
    </div>

    <div v-else>
      <!-- User Info (visible to all logged in users) -->
      <section class="profile-section">
        <h2>My Info</h2>
        <p><strong>First Name:</strong> {{ userInfo?.first_name || 'N/A' }}</p>
        <p><strong>Last Name:</strong> {{ userInfo?.last_name || 'N/A' }}</p>
        <p><strong>Email:</strong> {{ userInfo?.email || 'N/A' }}</p>
      </section>

      <!-- My Reservations (only for clients) -->
      <section v-if="isClient" class="profile-section">
        <h2>My Reservations</h2>
        <div v-if="reservations.length" class="cards-container">
          <div v-for="res in reservations" :key="res.reservation_id" class="card">
            <p><strong>Training:</strong> {{ res.training_name }}</p>
            <p><strong>Session:</strong> {{ res.session_start_time ? new Date(res.session_start_time).toLocaleString() : 'N/A' }}
              - {{ res.session_end_time ? new Date(res.session_end_time).toLocaleString() : 'N/A' }}</p>
            <p><strong>Reservation Date:</strong> {{ res.reservation_date }}</p>
            <p><strong>Status:</strong> {{ res.status }}</p>
            <button v-if="res.status === 'RESERVED'" @click="cancelReservation(res.reservation_id)">Cancel</button>
          </div>
        </div>
        <p v-else>No reservations found.</p>
      </section>

      <!-- My Attendances (only for clients) -->
      <section v-if="isClient" class="profile-section">
        <h2>My Attendances</h2>
        <div v-if="attendances.length" class="cards-container">
          <div v-for="att in attendances" :key="att.attendance_id" class="card">
            <p><strong>Training:</strong> {{ att.training_name }}</p>
            <p><strong>Session:</strong> {{ new Date(att.session_start_time).toLocaleString() }} - {{ new Date(att.session_end_time).toLocaleString() }}</p>
            <p><strong>Attendance Date:</strong> {{ att.attendance_date }}</p>
            <p><strong>Status:</strong> {{ att.attendance_status }}</p>
            <p v-if="att.training_rating"><strong>Rating:</strong> {{ att.training_rating }}/10</p>
            <div v-else class="rate-container">
              <input type="number" v-model.number="att.newRating" min="1" max="10" placeholder="1-10"/>
              <button @click="rateAttendance(att.attendance_id, att.newRating)">Rate</button>
            </div>
          </div>
        </div>
        <p v-else>No attendances found.</p>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userId: localStorage.getItem("userId"),
      userType: localStorage.getItem("userType"),
      userInfo: null,
      reservations: [],
      attendances: []
    };
  },
  computed: {
    isClient() {
      return this.userType === "CLIENT";
    }
  },
  methods: {
    async fetchUserInfo() {
      if (!this.userId) return;
      try {
        const res = await axios.get(`http://localhost:8000/users/${this.userId}`);
        this.userInfo = res.data;
      } catch (error) {
        console.error("Error fetching user info:", error.response?.data || error.message);
      }
    },
    async fetchReservations() {
      if (!this.isClient) return;
      try {
        const res = await axios.get(`http://localhost:8000/reservations/client/${this.userId}`);
        this.reservations = res.data;
      } catch (error) {
        console.error("Error fetching reservations:", error.response?.data || error.message);
      }
    },
    async fetchAttendances() {
      if (!this.isClient) return;
      try {
        const res = await axios.get(`http://localhost:8000/attendances/client/${this.userId}`);
        this.attendances = res.data;
      } catch (error) {
        console.error("Error fetching attendances:", error.response?.data || error.message);
      }
    },
    async cancelReservation(reservationId) {
      try {
        await axios.put(`http://127.0.0.1:8000/reservations/${reservationId}/cancel`);
        this.fetchReservations();
      } catch (error) {
        console.error("Error cancelling reservation:", error.response?.data || error.message);
      }
    },
    async rateAttendance(attendanceId, rating) {
      if (!rating || rating < 1 || rating > 10) {
        alert("Rating must be between 1 and 10");
        return;
      }
      try {
        await axios.put(`http://127.0.0.1:8000/attendances/${attendanceId}`, {
          training_rating: rating
        });
        this.fetchAttendances();
      } catch (error) {
        console.error("Error rating attendance:", error.response?.data || error.message);
      }
    }
  },
   created() {
    if (this.userId) {
      this.fetchUserInfo();
      if (this.isClient) {
        this.fetchReservations();
        this.fetchAttendances();
      }
    }
  }
};
</script>

<style>
.profile-view {
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

.profile-section {
  width: 90%;
  max-width: 900px;
  margin-bottom: 40px;
}

.cards-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  padding: 20px;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card button {
  width: 120px;
  padding: 8px;
  border: none;
  border-radius: 5px;
  background-color: rgb(0, 100, 180);
  color: #fff;
  cursor: pointer;
  transition: 0.2s;
}

.card button:hover {
  background-color: rgb(0, 80, 150);
}

.rate-container {
  display: flex;
  gap: 10px;
  align-items: center;
}

.rate-container input {
  width: 60px;
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}
</style>
