<template>
  <div>
    <h1>Danh sách nhà cung cấp</h1>
    <form @submit.prevent="addSupplier">
      <input v-model="newSupplier.name" placeholder="Tên nhà cung cấp" required />
      <input v-model="newSupplier.phone" placeholder="Số điện thoại" />
      <input v-model="newSupplier.email" placeholder="Email" />
      <input v-model="newSupplier.address" placeholder="Địa chỉ" />
      <button type="submit">Thêm nhà cung cấp</button>
    </form>

    <ul>
      <li v-for="supplier in suppliers" :key="supplier.id">
        <span>{{ supplier.name }} - {{ supplier.phone }} - {{ supplier.email }} - {{ supplier.address }}</span>
        <button @click="editSupplier(supplier)">Sửa</button>
        <button @click="deleteSupplier(supplier.id)">Xóa</button>
      </li>
    </ul>

    <div v-if="editingSupplier">
      <h2>Sửa nhà cung cấp</h2>
      <form @submit.prevent="updateSupplier">
        <input v-model="editingSupplier.name" required />
        <input v-model="editingSupplier.phone" />
        <input v-model="editingSupplier.email" />
        <input v-model="editingSupplier.address" />
        <button type="submit">Cập nhật</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      suppliers: [],
      newSupplier: {
        name: '',
        phone: '',
        email: '',
        address: ''
      },
      editingSupplier: null
    };
  },
  methods: {
    fetchSuppliers() {
      axios.get('http://localhost:8000/api/suppliers/')
        .then(response => {
          this.suppliers = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addSupplier() {
      axios.post('http://localhost:8000/api/suppliers/', this.newSupplier)
        .then(response => {
          this.suppliers.push(response.data);
          this.newSupplier = { name: '', phone: '', email: '', address: '' };
        })
        .catch(error => {
          console.error(error);
        });
    },
    editSupplier(supplier) {
      this.editingSupplier = { ...supplier };
    },
    updateSupplier() {
      axios.put(`http://localhost:8000/api/suppliers/${this.editingSupplier.id}/`, this.editingSupplier)
        .then(response => {
          const index = this.suppliers.findIndex(s => s.id === this.editingSupplier.id);
          this.suppliers.splice(index, 1, response.data);
          this.editingSupplier = null;
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteSupplier(id) {
      axios.delete(`http://localhost:8000/api/suppliers/${id}/`)
        .then(() => {
          this.suppliers = this.suppliers.filter(supplier => supplier.id !== id);
        })
        .catch(error => {
          console.error(error);
        });
    }
  },
  mounted() {
    this.fetchSuppliers();
  }
};
</script>

<style scoped>
/* Thêm CSS nếu cần */
</style>