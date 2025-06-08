import redis
import logging

# Konfigurasi logging
logging.basicConfig(filename='./redis_data_fetch.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Koneksi ke Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    # Ambil semua kunci
    keys = redis_client.keys("*")
    
    if not keys:
        logging.info("Tidak ada kunci ditemukan di Redis")
    else:
        logging.info(f"Ditemukan {len(keys)} kunci di Redis")
        for key in keys:
            # Ambil tipe data kunci
            key_type = redis_client.type(key)
            # Ambil nilai berdasarkan tipe data
            if key_type == "string":
                value = redis_client.get(key)
            elif key_type == "list":
                value = redis_client.lrange(key, 0, -1)
            elif key_type == "set":
                value = list(redis_client.smembers(key))
            elif key_type == "zset":
                value = redis_client.zrange(key, 0, -1, withscores=True)
            elif key_type == "hash":
                value = redis_client.hgetall(key)
            else:
                value = "Tipe data tidak didukung"
            
            # Ambil TTL
            ttl = redis_client.ttl(key)
            logging.info(f"Kunci: {key}, Tipe: {key_type}, Nilai: {value}, TTL: {ttl} detik")

except redis.RedisError as e:
    logging.error(f"Terjadi kesalahan saat mengakses Redis: {e}")