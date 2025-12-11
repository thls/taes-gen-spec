class CacheStore
  # @param key [String] cannot be empty
  # @param value [Object]
  # @return [Boolean] true if the key-value pair was successfully stored in the cache
  # @return [Boolean] false if the storage operation failed
  def set(key, value)
    # TODO
  end

  # @param key [String]
  # @return [Object, nil] the cached value associated with the key if it exists
  # @return [nil] nil if the key does not exist in the cache
  def get(key)
    # TODO
  end

end