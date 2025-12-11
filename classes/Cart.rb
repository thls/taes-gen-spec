class Cart
  # @param product_id [Integer]
  # @param quantity [Integer] must be >= 1
  # @return [NilClass] nil after successfully adding the item to the cart
  # @raise [ArgumentError] the param quantity is less than 1
  def add_item(product_id, quantity)
    # TODO
  end

  # @param product_id [Integer]
  # @return [NilClass] nil after successfully removing the item from the cart
  def remove_item(product_id)
    # TODO
  end

  # @return [Float] the total price of all items in the cart as a float
  # @return [Float] 0.0 if the cart is empty
  def total_price()
    # TODO
  end

  # @param id [String]
  # @param qty [Integer] must be >= 1
  # @return [Integer] the add item result as an integer
  def add_item(id, qty)
    # TODO
  end

  # @param id [String]
  # @return [Integer] the remove item result as an integer
  def remove_item(id)
    # TODO
  end

end