class BillingService
  # @param amount [Float] must be > 0
  # @param currency [String]
  # @return [Boolean] true if the charge was successfully processed
  # @return [Boolean] false if the charge failed due to insufficient funds or payment gateway error
  # @raise [ArgumentError] the param amount is less than or equal to zero
  def charge(amount, currency)
    # TODO
  end

  # @param transaction_id [String]
  # @return [Boolean] true if the refund was successfully processed
  # @return [Boolean] false if the transaction_id does not exist or the refund failed
  def refund(transaction_id)
    # TODO
  end

end