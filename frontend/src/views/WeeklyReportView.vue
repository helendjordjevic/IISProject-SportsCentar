<template>
  <div class="container mt-4">
    <h2>Weekly Training Report</h2>
    <p>Select week start date to view report</p>

    <div class="mb-3">
      <label for="weekStart" class="form-label">Week Start Date:</label>
      <input 
        type="date" 
        id="weekStart" 
        v-model="selectedWeekStart"
        class="form-control"
      />
      <button class="btn btn-primary mt-2" @click="fetchReport">
        Load Report
      </button>
    </div>

    <div v-if="loading" class="text-center my-4">
      Loading report...
    </div>

    <div v-else>
      <table class="table table-striped" v-if="reportData.length">
        <thead>
          <tr>
            <th>Session ID</th>
            <th>Training Name</th>
            <th>Instructor</th>
            <th>Studio</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Attended</th>
            <th>Average Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in reportData" :key="session.session_id">
            <td>{{ session.session_id }}</td>
            <td>{{ session.training_name }}</td>
            <td>{{ session.instructor_name }}</td>
            <td>{{ session.training_studio_number }}</td>
            <td>{{ formatDateTime(session.session_start_time) }}</td>
            <td>{{ formatDateTime(session.session_end_time) }}</td>
            <td>{{ session.attended_count }}</td>
            <td>{{ session.average_rating ?? '-' }}</td>
          </tr>
        </tbody>
      </table>

      <p v-else>No sessions found for this week.</p>

       <div v-if="reportData.length" class="mt-3">
        <button class="btn btn-success" @click="downloadPDF">
          Download PDF
        </button>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      reportData: [],
      loading: false,
      selectedWeekStart: null, 
    };
  },
  methods: {
    fetchReport() {
      if (!this.selectedWeekStart) {
        alert("Please select a week start date");
        return;
      }

      this.loading = true;

      axios.get("http://localhost:8000/attendances/reports/weekly", {
        params: { week_start_date: this.selectedWeekStart }
      })

      .then(res => {
        this.reportData = res.data;
      })
      .catch(err => {
        console.error("Error fetching weekly report:", err);
        alert("Failed to load report");
      })
      .finally(() => {
        this.loading = false;
      });
    },
    async downloadPDF() {
      if (!this.selectedWeekStart) {
        alert("Please select a week start date");
        return;
      }

      try {
        const response = await axios.get(
          "http://localhost:8000/attendances/reports/weekly/pdf",
          {
            params: { week_start_date: this.selectedWeekStart },
            responseType: "blob", 
          }
        );

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", `weekly_report_${this.selectedWeekStart}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (err) {
        console.error("Error downloading PDF:", err);
        alert("Failed to download PDF");
      }
    },
    formatDateTime(dt) {
      const d = new Date(dt);
      return d.toLocaleString();
    }
  }
};
</script>

<style scoped>
h2 {
  color: #0078c8;
}
</style>
