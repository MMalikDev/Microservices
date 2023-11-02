import { apiEndpoints } from '$lib/data/api.js';

async function getProducts() {
	const response = await fetch(apiEndpoints.PRODUCTS);
	const content = await response.json();
	return content;
}

async function getOrders() {
	const response = await fetch(apiEndpoints.ORDERS);
	const content = await response.json();
	return content;
}

export { getProducts, getOrders };
