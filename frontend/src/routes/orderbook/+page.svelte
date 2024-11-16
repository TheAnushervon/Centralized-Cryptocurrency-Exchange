<script>
  import { onMount } from 'svelte';
  import { writable } from 'svelte/store';

  let orders = writable({ bids: [], asks: [] });
  let error = writable(null);
  let showModal = writable(false);

  let selectedCoin = 'BTC';
  let usdRate = 1; // You can enhance this by fetching live conversion rates.

  const toggleModal = () => showModal.update(v => !v);

  const addOrder = (type, price, qty) => {
    orders.update(currentOrders => {
      if (type === 'buy') {
        currentOrders.bids.push({ price, qty });
      } else if (type === 'sell') {
        currentOrders.asks.push({ price, qty });
      }
      return currentOrders;
    });
    toggleModal();
  };

  async function handlePlaceOrder(type, price, qty, coin) {
    const token = localStorage.getItem("access_token");
    const endpoint = `http://localhost:8000/api/orders/place`;
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ type, price, qty, coin })
    });
    if (response.ok) {
      type = '';
      price = '';
      qty = '';
    } else {
      console.error('Withdrawal failed');
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    const form = event.target;
    const type = form.type.value;
    const price = form.price.value;
    const qty = form.qty.value;
    const coin = form.coin.value;

    if (price && qty) {
      addOrder(type, price, qty);
      handlePlaceOrder(type, price, qty, coin); // Call handlePlaceOrder with the correct values
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
          <th>≈USD</th>
        </tr>
      </thead>
      <tbody>
        {#each $orders.asks as { price, qty }}
          <tr class="sell">
            <td>{price}</td>
            <td>{qty}</td>
            <td>{(+price * +qty).toFixed(2)}</td>
            <td>{(usdRate * +price * +qty).toFixed(2)}</td>
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
          <th>≈USD</th>
        </tr>
      </thead>
      <tbody>
        {#each $orders.bids as { price, qty }}
          <tr class="buy">
            <td>{price}</td>
            <td>{qty}</td>
            <td>{(+price * +qty).toFixed(2)}</td>
            <td>{(usdRate * +price * +qty).toFixed(2)}</td>
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
