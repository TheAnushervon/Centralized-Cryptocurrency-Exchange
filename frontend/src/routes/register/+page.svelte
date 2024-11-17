<script>
    let email = '';
    let username = '';
    let password = '';
  
    async function handleRegister() {
      const response = await fetch('/api/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, username, password })
      });
      if (response.ok) {
        alert('Registration successful');
      } else {
        alert('Registration failed');
      }
    }
  </script>
  
  <main>
    <h1>Register</h1>
    <input bind:value={email} placeholder="Email" />
    <input bind:value={username} placeholder="Username" />
    <input bind:value={password} placeholder="Password" type="password" />
    <button on:click={handleRegister}>Register</button>
  </main>
  