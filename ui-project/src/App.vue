<template>
  <div id="app">
    <ApiInterface />
  </div>
</template>

<script>
import ApiInterface from './components/ApiInterface.vue';

export default {
  name: 'App',
  components: {
    ApiInterface,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>