<script>
	export let orders = [];
</script>

<div class="d-flex flex-column">
	<h1 class="text-center py-4 border-bottom">Order History</h1>

	<div class="table-responsive">
		<table class="table table-striped table-sm">
			<thead>
				<tr>
					<th scope="col">#</th>
					<th scope="col">Product ID</th>
					<th scope="col">Price</th>
					<th scope="col">Fee</th>
					<th scope="col">Total</th>
					<th scope="col">Quantity</th>
					<th scope="col">Status</th>
				</tr>
			</thead>

			{#each orders as order (order.id)}
				<tr key={order.id}>
					<td>{order.id}</td>
					<td>{order.product_id}</td>
					<td>{order.price.toFixed(2)}</td>
					<td>{order.fee.toFixed(2)}</td>
					<td>{order.total.toFixed(2)}</td>
					<td>{order.quantity}</td>
					<td>{order.status}</td>
				</tr>
			{/each}

			<tbody />
		</table>
	</div>
</div>
