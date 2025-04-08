import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Thay bằng URL API Django của bạn
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  getItems() {
    return apiClient.get('/items/'); // Giả sử endpoint của bạn là /items/
  },
  createItem(data) {
    return apiClient.post('/items/', data);
  },
  // Thêm các phương thức khác như update, delete nếu cần
};