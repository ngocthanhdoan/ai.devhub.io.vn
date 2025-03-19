<template>
  <div class="api-interface">
    <h1>API Interface</h1>
    <div class="button-group">
      <button @click="fetchData" class="btn">Get Data</button>
      <button @click="sendData" class="btn">Post Data</button>
      <button @click="fetchStats" class="btn">Get Stats</button>
      <button @click="checkHealth" class="btn">Health Check</button>
    </div>
    <div v-if="response" class="response-container">
      <h2>Response:</h2>
      <pre>
      <code>{{ JSON.stringify(response, null, 2).trim() }}</code>
      </pre>
    </div>
  </div>
</template>

<script>
import { getData, postData, getStats, healthCheck } from '../plugins/api';

export default {
  data() {
    return {
      response: null,
    };
  },
  methods: {
    async fetchData() {
      this.response = await getData();
    },
    async sendData() {
      const data = { message: 'Hello from Vue!' };
      this.response = await postData(data);
    },
    async fetchStats() {
      this.response = await getStats();
    },
    async checkHealth() {
      this.response = await healthCheck();
    },
  },
};
</script>

<style scoped>
.api-interface {
  font-family: Arial, sans-serif;
  text-align: center;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 40px auto;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

.response-container {
  margin-top: 20px;
  text-align: left;
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #ddd;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

pre {
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0;
}

h2 {
  color: #555;
  margin-bottom: 10px;
}
</style>