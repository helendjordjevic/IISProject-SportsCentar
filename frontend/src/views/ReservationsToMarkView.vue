<template>
  <div class="reservations-to-mark">
    <h1>Mark Attendances — {{ session.training_name }} ({{ session.session_start_time | formatDate }})</h1>

    <div v-if="reservations.length">
      <div v-for="res in reservations" :key="res.client_id" class="reservation-card">
        <p><strong>Client:</strong> {{ res.client_name }}</p>
        <p v-if="res.attendance_marked"><strong>Status:</strong> {{ res.attendance_status }}</p>
        <div v-else>
          <button @click="markAttendance(res, 'ATTENDED')" class="attended-btn">Attended</button>
          <button @click="markAttendance(res, 'NOT_ATTENDED')" class="not-attended-btn">Not Attended</button>
        </div>
      </div>
    </div>
    <div v-else>
      <p>No reservations for this session.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      session: {},
      reservations: []
    };
  },
  filters: {
    formatDate(value) {
      if (!value) return '';
      return new Date(value).toLocaleString();
    }
  },
  methods: {
    async fetchReservations() {
      const sessionId = this.$route.params.sessionId;
      try {
        const res = await axios.get(`http://localhost:8000/reservations/session/${sessionId}/to_mark`);
        this.reservations = res.data;
        if (this.reservations.length > 0) {
          this.session = {
            training_name: this.reservations[0].training_name,
            session_start_time: this.reservations[0].session_start_time
          };
        }
      } catch (err) {
        console.error("Error fetching reservations:", err);
      }
    },
    async markAttendance(reservation, status) {
      try {
        const payload = {
          client_id: reservation.client_id,
          session_id: reservation.session_id,
          attendance_status: status,
          attendance_date: new Date(reservation.session_end_time).toISOString().split('T')[0]
        };

        await axios.post("http://localhost:8000/attendances/", payload);

        reservation.attendance_marked = true;
        reservation.attendance_status = status;

      } catch (err) {
        // Ako već postoji, update-uj
        if (err.response && err.response.data.detail === "Attendance already recorded for this session") {
          const attendanceId = reservation.attendance_id;
          await axios.put(`http://localhost:8000/attendances/${attendanceId}`, { attendance_status: status });
          reservation.attendance_marked = true;
          reservation.attendance_status = status;
        } else {
          console.error(err);
          alert("Greška prilikom markiranja prisustva");
        }
      }
    }
  },
  created() {
    this.fetchReservations();
  }
};
</script>

<style scoped>
.reservation-card {
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 10px;
}
.attended-btn {
  background-color: green;
  color: white;
  margin-right: 5px;
  padding: 5px 10px;
  border-radius: 5px;
}
.not-attended-btn {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
