import apiClient from "./repository";

export default {
  getAllProducts() {
    return apiClient.get("/products/");
  },
  getProductById(id) {
    return apiClient.get(`/products/${id}/`);
  },
  createProduct(productData) {
    return apiClient.post("/products/", productData);
  },
  updateProduct(id, productData) {
    return apiClient.put(`/products/${id}/`, productData);
  },
  deleteProduct(id) {
    return apiClient.delete(`/products/${id}/`);
  },
};
