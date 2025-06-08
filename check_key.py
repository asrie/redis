import redis
import logging

# Konfigurasi logging
logging.basicConfig(filename='./redis_ttl_update.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Koneksi ke Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    # Ambil semua kunci
    keys = redis_client.keys("*")
    
    if not keys:
        logging.info("Tidak ada kunci ditemukan di Redis")
    else:
        for key in keys:
            # Cek TTL dari kunci
            ttl = redis_client.ttl(key)
            logging.info("TTL untuk kunci '%s' adalah: %d detik" % (key, ttl))

            # Jika TTL = -1 (tidak ada kadaluarsa), ubah ke 5 detik
            if ttl == -1:
                redis_client.expire(key, 300)
                logging.info("TTL untuk kunci '%s' telah diubah menjadi 5 menit" % key)
            elif ttl == -2:
                logging.warning("Kunci '%s' tidak ditemukan di Redis" % key)
            else:
                logging.info("Kunci '%s' sudah memiliki TTL: %d detik, tidak diubah" % (key, ttl))

            # Verifikasi TTL setelah perubahan
            new_ttl = redis_client.ttl(key)
            logging.info("TTL baru untuk kunci '%s' adalah: %d menit" % (key, new_ttl))

except redis.RedisError as e:
    logging.error(f"Terjadi kesalahan saat mengakses Redis: {e}")