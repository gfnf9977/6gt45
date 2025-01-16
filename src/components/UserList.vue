<template>
  <div class="user-list-container">
    <h1 class="title">Список користувачів</h1>
    <div class="add-user-container">
      <input v-model="newUser" placeholder="Додати користувача" class="input" />
      <button @click="addUser" class="button add-button">Додати</button>
    </div>
    <ul v-if="users.length" class="user-list">
      <li v-for="user in users" :key="user.id" class="user-item">
        {{ user.username }}
        <button @click="deleteUser(user.id)" class="button delete-button">Видалити</button>
      </li>
    </ul>
    <p v-else class="no-users">Немає користувачів у базі даних</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
      newUser: ''
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
    async addUser() {
      try {
        await axios.post('http://localhost:5000/api/users', {username: this.newUser});
        this.newUser = '';
        this.fetchUsers();  // Оновлення списку користувачів після додавання
      } catch (error) {
        console.error('Помилка при додаванні користувача:', error);
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
.user-list-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.add-user-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.input {
  flex: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.add-button {
  background-color: #28a745;
  color: white;
}

.add-button:hover {
  background-color: #218838;
}

.delete-button {
  background-color: #dc3545;
  color: white;
}

.delete-button:hover {
  background-color: #c82333;
}

.user-list {
  list-style-type: none;
  padding: 0;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.no-users {
  text-align: center;
  color: #888;
}
</style>
