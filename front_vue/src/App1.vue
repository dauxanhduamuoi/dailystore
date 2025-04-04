<script setup>
// import HelloWorld from './components/HelloWorld.vue'
// import TheWelcome from './components/TheWelcome.vue'
import Home   from './components/Home.vue'
import ItemList from './components/ItemList.vue';
</script>

<template>
<!-- <RouterView><div class="app-container"><Home/></div>
  <div class="app-container"><ItemList/></div></RouterView> -->
<RouterView></RouterView>

</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>

<script>
import axios from 'axios'; // Import axios để gọi API

export default {
  name: 'App',
  data() {
    return {
      products: [] // Mảng lưu danh sách sản phẩm từ API
    };
  },
  mounted() {
    // Gọi API khi component được tải
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      // Gọi API từ backend Django
      axios
        .get('http://localhost:8000/api/products/') // URL của API
        .then(response => {
          this.products = response.data; // Gán dữ liệu từ API vào mảng products
        })
        .catch(error => {
          console.error('Có lỗi khi lấy dữ liệu:', error); // Xử lý lỗi nếu có
        });
    }
  }
};
</script>
