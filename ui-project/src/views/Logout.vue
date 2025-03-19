<template>
  <div class="logout-container">
    <h2 class="text-2xl font-bold mb-4">You have been logged out</h2>
    <button @click="handleLoginAgain" class="btn btn-primary">Login Again</button>
  </div>
</template>

<script>
export default {
  name: "Logout",
  methods: {
    handleLoginAgain() {
      this.$router.push("/login");
    },
  },
  mounted() {
    // Clear authentication state
    localStorage.removeItem("isAuthenticated");
  },
};
</script>

<style scoped>
.logout-container {
  text-align: center;
  margin-top: 50px;
}
</style>