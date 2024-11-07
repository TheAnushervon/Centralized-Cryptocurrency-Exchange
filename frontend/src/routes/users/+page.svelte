<script>
    import {UsersStore} from '../../users-store'
    import {onMount} from 'svelte'
    onMount (async function() {
        const endpoint = 'http://localhost:8000/api/get_users/'
        const response = await fetch (endpoint)
        const data = await response.json() 
        console.log(data) 
        UsersStore.set(data)
    })
</script>
<table>
    <thead>
      <tr>
        <th>Email</th>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Username</th>
        <th>ID</th>
        <th>Active</th>
        <th>Staff</th>
      </tr>
    </thead>
    <tbody>
      {#each $UsersStore as user (user.id)}
        <tr>
          <td>{user.email}</td>
          <td>{user.first_name}</td>
          <td>{user.last_name}</td>
          <td>{user.username}</td>
          <td>{user.id}</td>
          <td>{user.is_active ? 'Yes' : 'No'}</td>
          <td>{user.is_staff ? 'Yes' : 'No'}</td>
        </tr>
      {/each}
    </tbody>
  </table>