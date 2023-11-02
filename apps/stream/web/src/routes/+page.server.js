import { getProducts } from '$lib/data/index.js';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
	return {
		products: await getProducts()
	};
}
