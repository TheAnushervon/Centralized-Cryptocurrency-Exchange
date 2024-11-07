<script>
    import { onMount } from 'svelte';
  
    let orderbook = [];
  
    onMount(async () => {
      const response = await fetch('/api/orders');
      if (response.ok) {
        orderbook = await response.json();
      }
    });
  </script>
  
  <main>
    <h1>Order Book</h1>
    {#each orderbook as order}
      <div>
        <p>{order.type} Order - {order.quantity} at {order.price}</p>
      </div>
    {/each}
  </main>
  