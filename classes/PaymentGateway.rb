class PaymentGateway
  # @param amount [Float] must be positive
  # @param card [Object]
  # @return [String] a string representing the charge result
  # @raise [ArgumentError] the param amount is less than or equal to zero
  def charge(amount, card)
    # TODO
  end

  # @param transaction_id [String]
  # @return [Boolean] true if the payment operation was successful
  # @return [Boolean] false if the payment operation failed
  def refund(transaction_id)
    # TODO
  end

end