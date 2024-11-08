<script>
    import { onMount } from 'svelte';
  
    let isRegistering = false; // Toggle between login and registration
    let loginData = { email: '', password: '' };
    let registerData = { firstname: '', lastname: '', email: '', password: '' };
  
    // Toggle between login and registration
    function toggleForm() {
      isRegistering = !isRegistering;
    }
  
    // Placeholder functions for handling form submissions
    async function handleLogin() {
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      });
      const result = await response.json();
      // Handle the login response here
      console.log('Login response:', result);
    }
  
    async function handleRegister() {
      const response = await fetch('http://localhost:8000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(registerData),
      });
      const result = await response.json();
      // Handle the registration response here
      console.log('Registration response:', result);
    }
  </script>
  
  <style>
    .auth-container {
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
    }
  
    .auth-button:hover {
      background-color: #0056b3;
    }
  
    .toggle-link {
      margin-top: 10px;
      color: #007bff;
      cursor: pointer;
      text-align: center;
    }
  </style>
  
  <div class="auth-container">
    <div class="form-box">
      <h2>{isRegistering ? 'Register' : 'Login'}</h2>
  
      {#if isRegistering}
        <!-- Registration Form -->
        <div class="input-group">
          <label for="firstname">First Name</label>
          <input id="firstname" type="text" bind:value={registerData.firstname} placeholder="First Name" />
        </div>
  
        <div class="input-group">
          <label for="lastname">Last Name</label>
          <input id="lastname" type="text" bind:value={registerData.lastname} placeholder="Last Name" />
        </div>
  
        <div class="input-group">
          <label for="email">Email</label>
          <input id="email" type="email" bind:value={registerData.email} placeholder="Email" />
        </div>
  
        <div class="input-group">
          <label for="password">Password</label>
          <input id="password" type="password" bind:value={registerData.password} placeholder="Password" />
        </div>
  
        <button class="auth-button" on:click={handleRegister}>Register</button>
      {:else}
        <!-- Login Form -->
        <div class="input-group">
          <label for="email">Email</label>
          <input id="email" type="email" bind:value={loginData.email} placeholder="Email" />
        </div>
  
        <div class="input-group">
          <label for="password">Password</label>
          <input id="password" type="password" bind:value={loginData.password} placeholder="Password" />
        </div>
  
        <button class="auth-button" on:click={handleLogin}>Login</button>
      {/if}
  
      <div class="toggle-link" on:click={toggleForm}>
        {isRegistering ? 'Already have an account? Login' : 'New user? Register'}
      </div>
    </div>
  </div>
  