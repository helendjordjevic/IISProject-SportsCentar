<template>
  <div class="training-detail">
    <h1>{{ training.name }}</h1>
    <p>{{ training.description }}</p>

    <button 
      v-if="isAdmin" 
      @click="goToAddSession" 
      class="add-session-btn">
      Add Session
    </button>

    <h2>Dostupni termini</h2>
    <div v-if="sessions.length">
      <div v-for="session in sessions" :key="session.session_id" class="session-card">
        <p><strong>Početak:</strong> {{ new Date(session.start_time).toLocaleString() }}</p>
        <p><strong>Kraj:</strong> {{ new Date(session.end_time).toLocaleString() }}</p>
        <button 
          v-if="isClient" 
          @click="reserveSession(session.session_id)" 
          class="reserve-btn">          
          Reserve
        </button>
        <button
          v-if="isInstructor && isSessionFinished(session)"
          @click="goToReservationsToMark(session.session_id)"
           class="reserve-btn"
          style="background-color: rgb(240, 150, 0); margin-left: 5px;">
          Mark Attendances
        </button>
    </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
  data() {
    return {
      training: {},
      sessions: [],
      attendanceList: [],  // lista rezervacija za markiranje
      showAttendanceModal: false,
      selectedSessionId: null
    };
  }, 
  computed: {
    isClient() {
      return localStorage.getItem("userType") === "CLIENT";
    },
    isAdmin() {
      return localStorage.getItem("userType") === "ADMIN";
    },
    isInstructor() {
      return localStorage.getItem("userType") === "INSTRUCTOR";
    }
  },
 methods: {
  async fetchTrainingDetails() {
    const trainingId = this.$route.params.id;
    try {
      const trainingResponse = await axios.get(`http://localhost:8000/trainings/${trainingId}`);
      this.training = trainingResponse.data;

      const sessionsResponse = await axios.get(`http://localhost:8000/sessions/training/${trainingId}`);
      this.sessions = sessionsResponse.data;
    } catch (error) {
      console.error("Error fetching training details or sessions:", error);
    }
  },
  goToAddSession() {
    const trainingId = this.$route.params.id;
    this.$router.push({ name: "addSession", params: { trainingId } });
  },
   goToReservationsToMark(sessionId) {
    this.$router.push({ name: "reservationsToMark", params: { sessionId } });
  },

  isSessionFinished(session) {
    const now = new Date();
    const sessionEnd = new Date(session.end_time);
    return now >= sessionEnd;
  },

  async reserveSession(sessionId) {
    const userEmail = localStorage.getItem("userEmail");
    const userType = localStorage.getItem("userType");
    const userId = localStorage.getItem("userId");

    if (!userEmail || !userId) {
      await Swal.fire({
        title: "Need to sign in",
        text: "You need to sign in to reserve a session.",
        icon: "warning",
        confirmButtonColor: "rgb(0, 175, 240)"
      });
      this.$router.push("/login");
      return;
    }

    if (userType !== "CLIENT") {
      await Swal.fire({
        title: "Cannot reserve",
        text: "Only clients can reserve sessions.",
        icon: "error",
        confirmButtonColor: "rgb(0, 175, 240)"
      });
      return;
    }

    try {
      const reservationData = {
        client_id: parseInt(userId),
        session_id: sessionId,
        reservation_date: new Date().toISOString().split("T")[0]
      };

      await axios.post("http://localhost:8000/reservations/", reservationData);

      await Swal.fire({
        title: "Success",
        text: "Reservation successfully created!",
        icon: "success",
        confirmButtonColor: "rgb(0, 175, 240)"
      });

    } catch (error) {
  console.error("Reservation error:", error); 
  let message = "Došlo je do greške prilikom rezervacije.";

  if (error.response && error.response.data) {
    if (typeof error.response.data === 'string') {
      message = error.response.data; 
    } else if (error.response.data.message) {
      message = error.response.data.message; 
    } else {
      message = JSON.stringify(error.response.data); 
    }
  }
      await Swal.fire({
        title: "Reservation failed",
        text: message,
        icon: "error",
        confirmButtonColor: "rgb(0, 175, 240)"
      });
    }
  }
},

  created() {
    this.fetchTrainingDetails();
  }
};
</script>

<style>
.training-detail {
  padding: 40px;
  background-color: #F0F6F6;
  min-height: 100vh;
}

h1 {
  color: rgb(0, 100, 180);
  margin-bottom: 10px;
}

h2 {
  color: rgb(0, 80, 150);
  margin-top: 30px;
  margin-bottom: 10px;
}

.session-card {
  padding: 15px;
  border-radius: 10px;
  background-color: #fff;
  margin-bottom: 15px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.session-card:hover {
  transform: scale(1.02);
}

.reserve-btn {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: rgb(0, 175, 240);
  border: none;
  border-radius: 20px;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

.reserve-btn:hover {
  background-color: rgb(0, 145, 220);
}

.add-session-btn {
  margin: 20px 0;
  padding: 10px 15px;
  background-color: rgb(0, 180, 100);
  border: none;
  border-radius: 20px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-session-btn:hover {
  background-color: rgb(0, 140, 80);
}

</style>