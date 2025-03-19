<template>
  <div class="antialiased bg-gray-50 dark:bg-gray-900" v-if="isAuthenticated">
    <Header />
    <Sidebar />
    <main class="p-4 md:ml-64 h-auto pt-20">
     
      <router-view />

    </main>
    <Footer />
  </div>
  <div v-else>
    <div>
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Header from "./components/Header.vue";
import Sidebar from "./components/Sidebar.vue";
import Footer from "./components/Footer.vue";
import {
  initAccordions,
  initCarousels,
  initCollapses,
  initDials,
  initDismisses,
  initDrawers,
  initDropdowns,
  initModals,
  initPopovers,
  initTabs,
  initTooltips
} from 'flowbite';

const isLoggedIn = ref(false);
const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";

// initialize components based on data attribute selectors
onMounted(() => {
  initAccordions();
  initCarousels();
  initCollapses();
  initDials();
  initDismisses();
  initDrawers();
  initDropdowns();
  initModals();
  initPopovers();
  initTabs();
  initTooltips();
});
</script>
