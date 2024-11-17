<script>
  import { onMount, onDestroy } from 'svelte';
  import { writable } from 'svelte/store';

  let orders = writable({ bids: [], asks: [] });
  let error = writable(null);
  let showModal = writable(false);

  let selectedCoin = 'BTC';
  let usdRate = 1;
  let intervalId;

  const toggleModal = () => showModal.update(v => !v);

  const addOrder = (type, price, qty) => {
    orders.update(currentOrders => {
      if (type === 'buy') {
        return { ...currentOrders, bids: [...currentOrders.bids, { price, quantity: qty }] };
      } else if (type === 'sell') {
        return { ...currentOrders, asks: [...currentOrders.asks, { price, quantity: qty }] };
      }
      return currentOrders;
    });
  };

  async function handlePlaceOrder(type, price, qty, coin) {
    const token = localStorage.getItem("access_token");
    const endpoint = `http://localhost:8000/api/orders/place`;
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ type, price, qty, coin })
      });
      if (response.ok) {
        addOrder(type, price, qty);
        toggleModal();
        await GetOrders(); // Fetch latest orders after placing a new one
      } else {
        console.error('Order placement failed');
        error.set('Failed to place order');
      }
    } catch (err) {
      console.error('Error placing order:', err);
      error.set('Error placing order');
    }
  }

  async function GetOrders() {
    const token = localStorage.getItem("access_token");
    const endpoint = `http://localhost:8000/api/orders`;

    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        const bids = data.filter(order => order.type === 'buy');
        const asks = data.filter(order => order.type === 'sell');
        orders.set({ bids, asks });
      } else {
        console.error('Failed to fetch orders');
        error.set('Failed to fetch orders');
      }
    } catch (err) {
      console.error('Error fetching orders:', err);
      error.set('Error fetching orders');
    }
  }

  function startPolling() {
    GetOrders(); // Initial fetch
    intervalId = setInterval(GetOrders, 5000); // Fetch every 5 seconds
  }

  onMount(() => {
    startPolling();
  });

  onDestroy(() => {
    if (intervalId) clearInterval(intervalId);
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    const form = event.target;
    const type = form.type.value;
    const price = form.price.value;
    const qty = form.qty.value;
    const coin = form.coin.value;

    if (price && qty) {
      handlePlaceOrder(type, price, qty, coin);
      form.reset();
    } else {
      error.set('Please fill in all fields.');
    }
  };
</script>

<style>
  .orderbook { margin: 20px; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
  th, td { text-align: center; padding: 8px; border: 1px solid #ddd; }
  .sell { color: red; }
  .buy { color: green; }
  .responsive { overflow-x: auto; }
  .modal { display: block; position: fixed; top: 20%; left: 50%; transform: translate(-50%, 0); background: white; padding: 20px; border: 1px solid #ddd; box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3); z-index: 10; }
</style>

<div class="orderbook">
  <h1>Orderbook for {selectedCoin}/USDT</h1>
  {#if $error}
    <p class="error">{$error}</p>
  {/if}

  <div class="responsive">
    <table>
      <thead>
        <tr>
          <th>Price (USDT)</th>
          <th>Qty ({selectedCoin})</th>
          <th>Total ({selectedCoin})</th>
          
        </tr>
      </thead>
      <tbody>
        {#each $orders.asks as { price, quantity }}
          <tr class="sell">
            <td>{price}</td>
            <td>{quantity}</td>
            <td>{(+price * +quantity).toFixed(2)}</td>

          </tr>
        {/each}
      </tbody>
    </table>

    <table>
      <thead>
        <tr>
          <th>Price (USDT)</th>
          <th>Qty ({selectedCoin})</th>
          <th>Total ({selectedCoin})</th>
          
        </tr>
      </thead>
      <tbody>
        {#each $orders.bids as { price, quantity }}
          <tr class="buy">
            <td>{price}</td>
            <td>{quantity}</td>
            <td>{(+price * +quantity).toFixed(2)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  <button on:click={toggleModal}>Create New Order</button>

  {#if $showModal}
    <div class="modal">
      <h2>Create Order</h2>
      <form on:submit={handleSubmit}>
        <label for="type">Type:</label>
        <select id="type" name="type">
          <option value="buy">Buy</option>
          <option value="sell">Sell</option>
        </select>
        <label for="coin">Coin:</label>
        <input id="coin" type="text" name="coin" />
        <br>
        <label for="price">Price:</label>
        <input id="price" type="number" step="0.01" name="price" />
        <br>
        <label for="qty">Qty:</label>
        <input id="qty" type="number" step="0.0001" name="qty" />
        <br>
        <button type="button" on:click={toggleModal}>Cancel</button>
        <button type="submit">Submit</button>
      </form>
    </div>
  {/if}
</div>
