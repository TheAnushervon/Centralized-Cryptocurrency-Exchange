<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation'; 
    import { DashboardStore } from '../../dashboard-store';
    
    let user = {};
    let balances = [];  // Array to hold all currency balances as objects { type, amount }
  
    // Fetch user data from backend
    // async function fetchUserData() {
    //   const endpoint = 'http://localhost:8000/api/get_user';
    //   const response = await fetch(endpoint);
    //   const data = await response.json();
      
    //   user = {
    //     firstname: data[0].firstname,
    //     lastname: data[0].lastname,
    //     email: data[0].email,
    //     id: data[0].id
    //   };
    //   DashboardStore.set(user);
    //   id = data[0].id;
    // }
  
    async function fetchUserData() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        console.error("No token found, redirecting to login.");
        goto('/'); // Redirect to login
        return;
    }

    const endpoint = 'http://localhost:8000/api/get_user';
    const response = await fetch(endpoint, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        const data = await response.json();
        user = {
            firstname: data.firstname,
            lastname: data.lastname,
            email: data.email
        };
        DashboardStore.set(user);
        console.log("WORKING!")
    } else {
        console.error("Failed to fetch user data. Redirecting to login.");
        goto('/'); // Redirect to login if unauthorized
    }
}


    async function fetchBalance() {
      const token = localStorage.getItem("access_token");
      const endpoint = `http://localhost:8000/api/wallets/`;
      const response = await fetch(endpoint, {
        method: 'GET', 
        headers: {
          'Authorization': `Bearer ${token}`, 
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      
      // Populate the balances array with currency type and amount
      balances = data.map(item => ({
        type: item.currency,
        amount: item.balance
      }));
    }
  
    // Fetch user data on component mount
    onMount(fetchUserData);
  
    // Reactive statement to fetch balance only after id is available
    
      onMount(fetchBalance()) ;
    
  
    function handleDeposit() {
      // Navigate to deposit page
      goto('/deposit'); 
    }
  
    function handleWithdraw() {
      // Navigate to withdraw page
      goto('/withdraw'); 
    }
  
    function handleOrderbook() {
      // Navigate to orderbook page
      goto('/orderbook'); 
    }
    function handleLogOut(){
        // things for logging out
        goto('/')
    }
  </script>
  
  <style>
    .dashboard {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      background-color: #f0f2f5;
      padding: 20px;
    }
  
    .dashboard h2 {
      text-align: center;
      margin-bottom: 20px;
    }
  
    .balance-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); /* Dynamic columns */
      gap: 30px;
      justify-content: center;
      width: 80%; /* Constrained width */
      margin-top: 20px;
    }
  
    .balance-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      background-color: #fff;
      border: 1px solid #ddd;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
  
    .balance-item h3 {
      font-size: 18px;
      margin: 10px 0;
    }
  
    .balance-item p {
      font-size: 16px;
      color: #555;
    }
  
    button {
      padding: 12px 24px;
      margin: 20px 10px 0 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      background-color: #007bff;
      color: #fff;
      font-size: 16px;
    }
  
    button:hover {
      background-color: #0056b3;
    }
  
    .orderbook-button {
      position: absolute;
      top: 20px;
      right: 20px;
    }
    .log-out{
        position: absolute;
        top: 20px; 
        left: 20px ; 
    }
  </style>
  
  <div class="dashboard">
    <h2>{user.email || 'User'}'s Dashboard</h2>
  
    <div class="balance-grid">
      {#each balances as { type, amount }}
        <div class="balance-item">
          <h3>{type}</h3>
          <p>{amount}</p>
        </div>
      {/each}
    </div>
  
    <button on:click={handleDeposit}>Deposit</button>
    <button on:click={handleWithdraw}>Withdraw</button>
    <button class="orderbook-button" on:click={handleOrderbook}>Orderbook</button>
    <button class="log-out" on:click={handleLogOut}>Log-Out</button>
</div>
  