<template>
  <div>
    <h1>Список користувачів</h1>
    <ul v-if="users.length">
      <li v-for="user in users" :key="user.id">
        {{ user.username }}
        <button @click="deleteUser(user.id)">Видалити</button>
      </li>
    </ul>
    <p v-else>Немає користувачів у базі даних</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: []
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/api/users');
        this.users = response.data;
      } catch (error) {
        console.error('Помилка при отриманні користувачів:', error);
      }
    },
    async deleteUser(userId) {
      try {
        await axios.delete(`http://localhost:5000/api/users/${userId}`);
        this.fetchUsers();  // Оновлення списку користувачів після видалення
      } catch (error) {
        console.error('Помилка при видаленні користувача:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Додайте стилі за потребою */
</style>
