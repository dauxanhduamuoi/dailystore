<template>
    <div id="app">
      <h1>Danh sách Sách phải ra</h1>
      <ul>
        <li v-for="book in books" :key="book.id">
          {{ book.name }} - {{ book.price }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  // Import Axios
  import axios from 'axios';
  
  export default {
    data() {
      return {
        books: [], // Mảng để chứa dữ liệu từ API
      };
    },
    created() {
      // Gọi API khi component được tạo
      axios.get('http://localhost:8000/api/products/') // URL của API Django
        .then(response => {
          this.books = response.data; // Lưu dữ liệu vào mảng books
        })
        .catch(error => {
          console.log('Có lỗi khi gọi API:', error);
        });
    },
  };
  </script>
  
  <style scoped>
  /* Các style cho component */
  </style>
  