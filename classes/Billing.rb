class Billing
  # @param amount [Float] must be > 0
  # @param currency [String]
  # @return [Boolean] true if the payment operation was successful
  # @return [Boolean] false if the payment operation failed
  # @raise [ArgumentError] the param amount is less than or equal to zero
  def charge(amount, currency)
    # TODO
  end

  # @param transaction_id [String]
  # @return [Boolean] true if the payment operation was successful
  # @return [Boolean] false if the payment operation failed
  def refund(transaction_id)
    # TODO
  end

  # @param customer [String]
  # @param amount [Float]
  # @return [String] a string representing the invoice result
  def invoice(customer, amount)
    # TODO
  end

  # @param invoice_id [String]
  # @return [Boolean] true if the operation was successful
  # @return [Boolean] false if the operation failed or the resource does not exist
  def cancel(invoice_id)
    # TODO
  end

end