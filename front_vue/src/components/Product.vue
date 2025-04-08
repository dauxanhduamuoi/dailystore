<template>
  <div id="app">
    <h1>Danh sách sản phẩm</h1>
    <ul>
      <li v-for="product in products" :key="product.id">
        {{ product.name }} - {{ product.price }} VND - {{ `https://localhost:8000${product.image}` }}
        <img :src=" `http://localhost:8000${product.image}`  "  v-if="product.image">
        <img :src=" product.image "  v-if="product.image">
      </li>
    </ul>
  </div>
</template>

<!-- <script>
import axios from 'axios'; // Import thư viện axios

export default {
  name: 'Product', // Tên component
  data() {
    return {
      products: [] // Khởi tạo mảng rỗng để lưu sản phẩm
    };
  },
  mounted() {
    this.fetchProducts(); // Gọi hàm fetchProducts khi component được gắn vào DOM
  },
  methods: {
    fetchProducts() {
      axios
        .get('http://localhost:8000/api/products/') // Gửi yêu cầu GET tới API
        .then(response => {
          this.products = response.data; // Lưu dữ liệu trả về vào mảng products
        })
        .catch(error => {
          console.error('Có lỗi khi lấy dữ liệu:', error); // In lỗi ra console nếu thất bại
        });
    }
  }
};
</script> -->




<script>
import axios from 'axios';
export default {
  data() {
    return {
      products: {} // Đối tượng sản phẩm ban đầu rỗng
    };
  },
  mounted() {
    this.fetchProductData(); // Gọi API khi component được gắn vào DOM
  },
  methods: {
    async fetchProductData() {
      try {
        // Gọi API (giả sử bạn dùng axios hoặc fetch)
        const response = await axios.get('http://localhost:8000/api/products/'); // Thay URL_API_SẢN_PHẨM bằng URL thật
        this.products.image = `http://localhost:8000${response.data.image}`;
        this.products = response.data; // Lưu dữ liệu sản phẩm vào state
      } catch (error) {
        console.error('Error fetching product data:', error);
      }
    }
  }
};
</script>
<!-- <style>
#app {
  font-family: Arial, sans-serif; // Font chữ cho ứng dụng
  text-align: center; // Căn giữa nội dung
  margin-top: 60px; // Khoảng cách phía trên
}
ul {
  list-style-type: none; // Bỏ dấu đầu dòng của danh sách
  padding: 0; // Bỏ padding mặc định
}
li {
  padding: 10px; // Khoảng cách bên trong mỗi item
  border-bottom: 1px solid #ccc; // Đường viền dưới mỗi item
}
</style> -->