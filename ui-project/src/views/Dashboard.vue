<template>
  <section class="bg-white dark:bg-gray-900">
    <div class="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
        <div class="mr-auto place-self-center lg:col-span-7">
            <h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white">Payments tool for software companies</h1>
            <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">From checkout to global sales tax compliance, companies around the world use Flowbite to simplify their payment stack.</p>
            <a href="#" class="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900">
                Get started
                <svg class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
            </a>
            <a href="#" class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 dark:focus:ring-gray-800">
                Speak to Sales
            </a> 
        </div>
        <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
            <img src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/hero/phone-mockup.png" alt="mockup">
        </div>                
    </div>
</section>
  <main class="p-4 h-auto">
    <!-- Thống kê -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
      <FlowbiteCard 
        title="Total API Calls" 
        :value="12345" 
        icon="fas fa-chart-line" 
        color="blue"
        class="h-32"
      />
      <FlowbiteCard 
        title="Successful Calls" 
        :value="12000" 
        icon="fas fa-check-circle" 
        color="green"
        class="h-32"
      />
      <FlowbiteCard 
        title="Failed Calls" 
        :value="345" 
        icon="fas fa-times-circle" 
        color="red"
        class="h-32"
      />
      <FlowbiteCard 
        title="Pending Requests" 
        :value="230" 
        icon="fas fa-clock" 
        color="yellow"
        class="h-32"
      />
    </div>

    <!-- Biểu đồ API -->
    <div class="border-2 border-dashed rounded-lg border-gray-300 dark:border-gray-600 h-100 mb-4 p-4">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">API Calls Overview</h2>
      <canvas id="apiCallsChart" class="mx-auto"></canvas>
    </div>

    <!-- Hoạt động gần đây -->
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div class="card-table-container">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Recent Activities</h2>
        <table class="table-custom">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left">Date</th>
              <th class="px-4 py-2 text-left">Action</th>
              <th class="px-4 py-2 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr class="hover:bg-gray-50">
              <td class="px-4 py-2">2023-10-01</td>
              <td class="px-4 py-2">API Call</td>
              <td class="px-4 py-2"><span class="badge badge-success">Success</span></td>
            </tr>
            <tr class="hover:bg-gray-50">
              <td class="px-4 py-2">2023-10-01</td>
              <td class="px-4 py-2">API Call</td>
              <td class="px-4 py-2"><span class="badge badge-danger">Failed</span></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-table-container">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Customer API Services</h2>
        <table class="table-custom">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left">Service Name</th>
              <th class="px-4 py-2 text-left">Expiration Date</th>
            </tr>
          </thead>
          <tbody>
            <tr class="hover:bg-gray-50">
              <td class="px-4 py-2">DevHub API Basic</td>
              <td class="px-4 py-2">2024-01-01</td>
            </tr>
            <tr class="hover:bg-gray-50">
              <td class="px-4 py-2">DevHub API Pro</td>
              <td class="px-4 py-2">2024-06-15</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Biểu đồ & Thống kê thêm -->
    <div class="border-2 border-dashed rounded-lg border-gray-300 dark:border-gray-600 h-111 mb-4 p-4">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Additional Analytics</h2>
      <canvas id="extraChart"></canvas>
    </div>
  </main>
</template>

<script>
import { onMounted } from "vue";
import Chart from "chart.js/auto";
import FlowbiteCard from "../components/FlowbiteCard.vue";

export default {
  name: "Dashboard",
  components: { FlowbiteCard },
  setup() {
    onMounted(() => {
      const ctx = document.getElementById("apiCallsChart").getContext("2d");
      new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: ["Total", "Successful", "Failed"],
          datasets: [
            {
              label: "API Calls",
              data: [12345, 12000, 345],
              backgroundColor: ["#3b82f6", "#10b981", "#ef4444"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
            },
          },
        },
      });

      const ctx2 = document.getElementById("extraChart").getContext("2d");
      new Chart(ctx2, {
        type: "bar",
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May"],
          datasets: [
            {
              label: "API Usage",
              data: [3000, 4000, 3500, 5000, 4800],
              backgroundColor: "#3b82f6",
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true,
            },
          },
        },
      });
    });
  },
};
</script>

<style scoped>
/* Basic Styling */
body {
  font-family: 'Inter', sans-serif;
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
}

.card-table-container {
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  height: 18rem;
}

.table-custom {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  border: 1px solid #e5e7eb;
  font-size: 0.9rem;
  text-align: left;
}

thead {
  background-color: #f9fafb;
}

tbody tr:hover {
  background-color: #f3f4f6;
}

.badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: 600;
}

.badge-success {
  background-color: #10b981;
  color: white;
}

.badge-danger {
  background-color: #ef4444;
  color: white;
}

/* Media Queries for Mobile */
@media (max-width: 768px) {
  h2 {
    font-size: 1.25rem;
  }

  .card-value {
    font-size: 1.5rem;
  }

  th,
  td {
    font-size: 0.85rem;
    padding: 8px;
  }
}
</style>
