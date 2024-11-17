<script>
    import { onMount } from 'svelte';
  
    let profile = {};
  
    onMount(async () => {
      const response = await fetch('/api/get_users/');
      if (response.ok) {
        profile = await response.json();
      }
    });
  </script>
  
  <main>
    <h1>Profile</h1>
    <div>Email: {profile.email}</div>
    <div>Username: {profile.username}</div>
    <h1>Go to Orderbook</h1>
    <button on:click={() => goto('/orderbook')}>Go to Ordre Book</button> 
    
</main>
  