<script>
	import { page } from '$app/stores';
	const links = [
		{ href: '/checkout', text: 'Checkout' },
		{ href: '/', text: 'Products' },
		{ href: '/history', text: 'History' }
	];
</script>

<nav id="sidebarMenu" class="d-md-block col-md-3 col-lg-2 bg-body-tertiary sidebar collapse">
	<div class="position-sticky pt-3">
		<ul class="nav flex-column">
			{#each links as link (link.href)}
				<li class="nav-item">
					{#if link.href == $page.url.pathname}
						<a class="nav-link active" aria-current="page" href={link.href}> {link.text} </a>
					{:else}
						<a class="nav-link" aria-current="page" href={link.href}> {link.text} </a>
					{/if}
				</li>
			{/each}
		</ul>
	</div>
</nav>

<style>
	.sidebar {
		position: fixed;
		inset: 0 auto 0 0;
		z-index: 100; /* Behind the navbar */
		padding: 3rem 0 0; /* Height of navbar */
		box-shadow: inset 0 0 0.5rem 0 rgba(0, 0, 0, 0.3);
	}

	.sidebar .nav-link {
		font-weight: 500;
	}

	.sidebar .nav-link.active {
		color: #3333cc;
	}

	@media (max-width: 767.98px) {
		.sidebar {
			top: 5rem;
		}
	}
</style>
