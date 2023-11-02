<script>
	import Orders from '$lib/components/Orders.svelte';
	export let data = [];
	const { orders } = data;
</script>

<svelte:head>
	<title>Order History</title>
</svelte:head>

<Orders {orders} />
