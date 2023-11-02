<script>
	import { apiEndpoints } from '$lib/data/api.js';

	let name;
	let price;
	let quantity;
	let message;

	async function onSubmit(e) {
		e.preventDefault();

		const response = await fetch(apiEndpoints.EXTERNAL_PRODUCTS, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ name, price, quantity })
		});
		if (response.status == 201) {
			const content = await response.json();
			message = `New product added - ID: ${content.pk}`;
		} else {
			message = 'Your product could not be created :(';
		}
	}
</script>

<div class="py-5 text-center">
	<h2>Create New Product</h2>

	{#if typeof message !== 'undefined'}
		<p class="lead">{message}</p>
	{/if}
</div>

<form class="mt-3" on:submit={onSubmit}>
	<div class="form-floating pb-3">
		<input id="name" class="form-control" placeholder="Name" bind:value={name} />
		<label for="name">Name</label>
	</div>

	<div class="form-floating pb-3">
		<input id="price" type="number" class="form-control" placeholder="Price" bind:value={price} />
		<label for="price">Price</label>
	</div>

	<div class="form-floating pb-3">
		<input
			id="quantity"
			type="number"
			class="form-control"
			placeholder="Quantity"
			bind:value={quantity}
		/>
		<label for="quantity">Quantity</label>
	</div>

	<button class="w-100 btn btn-lg btn-primary" type="submit">Submit</button>
</form>
