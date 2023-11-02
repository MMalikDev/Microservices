<script>
	import { apiEndpoints } from '$lib/data/api.js';
	export let products = [];

	async function remove(id) {
		if (window.confirm('Are you sure to delete this record?')) {
			const url = `${apiEndpoints.EXTERNAL_PRODUCTS}/${id}`;
			await fetch(url, { method: 'DELETE' });
			products = products.filter((p) => p.id !== id);
		}
	}
</script>

<div class="d-flex flex-column">
	<h1 class="text-center py-4">Product Catalogue</h1>
	<div class="pt-3 pb-2 mb-3 border-bottom">
		<a href="/create" class="btn btn-sm btn-outline-secondary">Add</a>
	</div>

	<div class="table-responsive">
		<table class="table table-striped table-sm">
			<thead>
				<tr>
					<th scope="col">#</th>
					<th scope="col">Name</th>
					<th scope="col">Price</th>
					<th scope="col">Quantity</th>
					<th scope="col">Actions</th>
				</tr>
			</thead>

			{#each products as product (product.id)}
				<tr key={product.id}>
					<td>{product.id}</td>
					<td>{product.name}</td>
					<td>{product.price.toFixed(2)}</td>
					<td>{product.quantity}</td>
					<td>
						<button class="btn btn-sm btn-outline-secondary" on:click={() => remove(product.id)}>
							Delete
						</button>
					</td>
				</tr>
			{/each}

			<tbody />
		</table>
	</div>
</div>
