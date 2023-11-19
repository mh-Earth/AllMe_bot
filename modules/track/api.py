from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        print([result.scheme, result.netloc])
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Example usage:
url1 = "https://www.example.com"
url2 = "not_a_valid_url"

print(f"{url1} is a valid URL: {is_valid_url(url1)}")
print(f"{url2} is a valid URL: {is_valid_url(url2)}")

# amazon
# availability
# a-price-symbol | a-price-whole . a-price-decimal

# rokomari
# sell-price | figure stock-available