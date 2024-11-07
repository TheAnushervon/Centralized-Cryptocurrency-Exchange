<script>
    import { onMount } from 'svelte';
  
    let orders = [];
  
    onMount(async () => {
      const response = await fetch('/api/orders');
      if (response.ok) {
        orders = await response.json();
      }
    });
  </script>
  
  <main>
    <h1>Orders</h1>
    {#each orders as order}
      <div>
        <p>Type: {order.type}</p>
        <p>Price: {order.price}</p>
        <p>Quantity: {order.quantity}</p>
        <p>Status: {order.status}</p>
      </div>
    {/each}
  </main>
  