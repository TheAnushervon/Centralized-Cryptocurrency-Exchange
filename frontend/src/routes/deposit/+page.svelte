<script>
    let currency = '';
    let amount = '';
  
    async function handleDeposit() {
      const token = localStorage.getItem("access_token");
      const endpoint = 'http://localhost:8000/api/wallets/deposit/';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', 
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ currency, amount })
      });
  
      if (response.ok) {
        // Deposit successful, you can show a success message or redirect the user
        console.log('Deposit successful');

        currency = ''; 
        amount = ''; 
      } else {
        // Deposit failed, you can show an error message
        console.error('Deposit failed');
      }
    }
  </script>
  
  <style>
    .deposit-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      background-color: #f0f2f5;
      padding: 20px;
    }
  
    .form-box {
      width: 100%;
      max-width: 400px;
      padding: 20px;
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
  
    h2 {
      text-align: center;
      margin-bottom: 20px;
    }
  
    .input-group {
      margin-bottom: 15px;
      display: flex;
      flex-direction: column;
    }
  
    label {
      margin-bottom: 5px;
      font-size: 14px;
    }
  
    input {
      padding: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 16px;
    }
  
    .auth-button {
      width: 100%;
      padding: 10px;
      border: none;
      border-radius: 4px;
      background-color: #007bff;
      color: #fff;
      font-size: 16px;
      cursor: pointer;
      margin-top: 10px;
    }
  
    .auth-button:hover {
      background-color: #0056b3;
    }
  </style>
  
  <div class="deposit-container">
    <div class="form-box">
      <h2>Deposit</h2>
  
      <form on:submit|preventDefault={handleDeposit}>
       
  
        <div class="input-group">
          <label for="currency">Currency</label>
          <input id="currency" type="text" bind:value={currency} placeholder="Currency (e.g., USD)" />
        </div>
  
        <div class="input-group">
          <label for="amount">Amount</label>
          <input id="amount" type="number" bind:value={amount} placeholder="Amount" />
        </div>
  
        <button class="auth-button" type="submit">Deposit</button>
      </form>
    </div>
  </div>
  