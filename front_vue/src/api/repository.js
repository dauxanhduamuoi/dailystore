import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000/api", // Thay bằng URL của backend Django
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
