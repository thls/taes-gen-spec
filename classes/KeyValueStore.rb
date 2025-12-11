class KeyValueStore
  # @param key [String] must not be empty
  # @param value [Object]
  # @return [Boolean] true if the data was successfully written
  # @return [Boolean] false if writing failed
  def set(key, value)
    # TODO
  end

  # @param key [String]
  # @return [Object, nil] the get object if found
  # @return [nil] nil if not found
  def get(key)
    # TODO
  end

  # @param key [String]
  # @return [Boolean] true if the resource was successfully deleted
  # @return [Boolean] false if deletion failed or the resource does not exist
  def delete(key)
    # TODO
  end

end