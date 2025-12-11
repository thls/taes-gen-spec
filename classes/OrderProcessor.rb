class OrderProcessor
  # @param order_id [Integer] must be positive and exist in the system
  # @param payment_method [String] must be one of: credit_card, debit_card, paypal, bank_transfer
  # @param amount [Float] must be greater than zero and less than 1000000
  # @param currency [String] must be a valid ISO 4217 currency code
  # @param customer_id [Integer] must be positive
  # @return [Hash] a hash containing the transaction details if payment was successful
  # @return [Hash] a hash with error information if payment failed
  # @raise [ArgumentError] the param order_id is invalid or does not exist
  # @raise [ArgumentError] the param payment_method is not one of the supported methods
  # @raise [ArgumentError] the param amount is less than or equal to zero or exceeds the maximum limit
  # @raise [ArgumentError] the param currency is not a valid ISO 4217 currency code
  def process_payment(order_id, payment_method, amount, currency, customer_id)
    # TODO
  end

  # @param order [Object] must not be nil
  # @return [Boolean] true if the operation succeeded
  # @return [Boolean] false if the operation failed
  def process(order)
    # TODO
  end

  # @param order_id [Integer]
  # @return [Boolean] true if the operation succeeded
  # @return [Boolean] false if the operation failed
  def cancel(order_id)
    # TODO
  end

  # @param order_id [Integer]
  # @return [String] a string representing the status result
  def status(order_id)
    # TODO
  end

end