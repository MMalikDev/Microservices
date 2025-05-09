<script>
	import { apiEndpoints } from '$lib/data/api.js';
	import debounce from 'lodash/debounce';

	const delay = 300;
	const defaultMessage = 'Buy your favorite product';

	let message = defaultMessage;
	let insufficientQTY = false;
	let maxQuantity = 0;
	let quantity = 0;
	let price = 0;

	let product_id;
	let orderID;

	$: insufficientQTY = quantity > maxQuantity;
	$: getTotal(quantity);

	function getTotal() {
		if (insufficientQTY) {
			message = `Not enough product in stock`;
		} else {
			const total = parseFloat(price) * quantity * 1.2 || 0;
			message = total > 0 ? `Total price is $${total.toFixed(2)}` : defaultMessage;
		}
	}

	async function updateId() {
		try {
			if (product_id) {
				const response = await fetch(`${apiEndpoints.EXTERNAL_PRODUCTS}/${product_id}`);
				const content = await response.json();
				maxQuantity = content.quantity;
				price = content.price;
				orderID = undefined;
				getTotal();
			}
		} catch (e) {
			message = defaultMessage;
			console.error(e);
		}
	}

	async function onSubmit(e) {
		e.preventDefault();

		const response = await fetch(apiEndpoints.EXTERNAL_ORDERS, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ product_id, quantity })
		});

		if (response.status == 201) {
			const content = await response.json();
			message = 'Thank you for your purchase!';
			orderID = `Your Order ID is ${content.pk}`;
		} else {
			message = 'Your order could not be placed :(';
		}
	}

	const handleInput = debounce(async (e) => {
		product_id = e.target.value;
		await updateId();
	}, delay);
</script>

<div class="container">
	<div class="py-5 text-center">
		<h2>Checkout</h2>
		<p class="lead">{message}</p>
		{#if typeof orderID !== 'undefined'}
			<p class="lead">{orderID}</p>
		{/if}
	</div>

	<form on:submit={onSubmit}>
		<div class="row g-3">
			<div class="col-sm-6">
				<label for="productId" class="form-label">Product</label>
				<input id="productId" class="form-control" on:input={handleInput} />
			</div>

			<div class="col-sm-6">
				<label for="quantity" class="form-label">Quantity</label>
				<input id="quantity" type="number" class="form-control" bind:value={quantity} />
			</div>
		</div>

		<hr class="my-4" />

		<button class="w-100 btn btn-primary btn-lg" type="submit">Buy</button>
	</form>
</div>
