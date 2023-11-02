<script>
	import Header from '$lib/components/navigation/Header.svelte';
	import Sidebar from '$lib/components/navigation/Sidebar.svelte';
</script>

<div class="app">
	<Header />

	<div class="container-fluid">
		<Sidebar />

		<main id="main" class="ms-sm-auto px-md-4 col-md-9 col-lg-10">
			<slot />
		</main>
	</div>
</div>
