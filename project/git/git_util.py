import hashlib
import hmac

# From https://github.com/SwagLyrics/swaglyrics-backend/blob/35d23d0ba416e742e381da931d592ce6f58fc13f/issue_maker.py#L268
def is_valid_signature(x_hub_signature, data, private_key):
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)