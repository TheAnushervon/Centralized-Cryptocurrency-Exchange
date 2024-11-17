export async function fetchOrderBook(category = 'spot', symbol = 'BTCUSDT', limit = 25, retryCount = 3, retryDelay = 1000) {
    const url = new URL('https://api-testnet.bybit.com/v5/market/orderbook');
    url.searchParams.append('category', category);
    url.searchParams.append('symbol', symbol);
    url.searchParams.append('limit', limit);
  
    for (let attempt = 0; attempt < retryCount; attempt++) {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          if (response.status === 429) {
            // Rate limit hit, wait before retrying
            await new Promise(resolve => setTimeout(resolve, retryDelay * Math.pow(2, attempt)));
            continue;
          } else {
            throw new Error('Failed to fetch orderbook data');
          }
        }
        return response.json();
      } catch (error) {
        console.error('Error fetching orderbook data:', error);
        throw error;
      }
    }
    throw new Error('Max retry attempts reached');
  }
  