<template>
    <div>
      <h2>Danh sách Items</h2>
      <ul>
        <li v-for="item in items" :key="item.id">{{ item.name }}</li>
      </ul>
      <form @submit.prevent="addItem">
        <input v-model="newItem" placeholder="Thêm item mới" />
        <button type="submit">Thêm</button>
      </form>
    </div>
  </template>
  
  <script>
  import api from '@/services/api';
  
  export default {
    name: 'ItemList',
    data() {
      return {
        items: [],
        newItem: '',
      };
    },
    created() {
      this.fetchItems();
    },
    methods: {
      async fetchItems() {
        try {
          const response = await api.getItems();
          this.items = response.data;
        } catch (error) {
          console.error('Lỗi khi lấy dữ liệu:', error);
        }
      },
      async addItem() {
        if (this.newItem.trim()) {
          try {
            await api.createItem({ name: this.newItem });
            this.newItem = '';
            this.fetchItems(); // Làm mới danh sách
          } catch (error) {
            console.error('Lỗi khi thêm item:', error);
          }
        }
      },
    },
  };
  </script>
  
  <style scoped>
  ul {
    list-style-type: none;
  }
  </style>