import { getOrders } from '$lib/data/index.js';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
	return {
		orders: await getOrders()
	};
}
