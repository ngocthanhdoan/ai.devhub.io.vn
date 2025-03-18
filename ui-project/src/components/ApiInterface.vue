<template>
  <div>
    <h1>API Interface</h1>
    <button @click="fetchData">Get Data</button>
    <button @click="sendData">Post Data</button>
    <button @click="fetchStats">Get Stats</button>
    <button @click="checkHealth">Health Check</button>
    <div v-if="response">
      <pre>{{ response }}</pre>
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
button {
  margin: 5px;
}
</style>