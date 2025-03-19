<template>
    <footer class="footer bg-gray-800 text-white text-center py-3">
        <p>&copy; https://devhub.io.vn</p>
    </footer>
</template>

<script>
export default {
    name: "Footer",
};
</script>

<style scoped>
.footer {
    background-color: #2d3748; /* Tailwind's bg-gray-800 */
    color: #ffffff; /* Tailwind's text-white */
    text-align: center;
    padding: 1rem 0; /* Tailwind's py-3 */
}

.footer p {
    margin: 0;
    font-size: 1rem;
}
</style>