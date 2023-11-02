<script>
	import Products from '$lib/components/Products.svelte';
	export let data = [];
	const { products } = data;
</script>

<svelte:head>
	<title>Products</title>
</svelte:head>

<Products {products} />
