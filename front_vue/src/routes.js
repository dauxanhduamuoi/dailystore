import { createRouter, createWebHistory} from 'vue-router';
import Home from './components/Home.vue';
import ItemList from './components/ItemList.vue';
import Product from './components/Product.vue';
import Product_1 from './components/Product_1.vue';
const routes = [
{ path: '/', name: 'Home', component: Home},
{path: '/item', name: 'ItemList', component: ItemList},
{path: '/product', name: 'Product', component: Product},
{path: '/product_1', name: 'Product_1', component: Product_1},
    
];
const router = createRouter ({
    history: createWebHistory(),
    routes
});

export default router;
