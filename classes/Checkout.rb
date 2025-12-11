class Checkout
  # @param total [Float]
  # @param code [String]
  # @return [Float] the total amount after applying the discount if the coupon code is valid
  # @return [Float] the original total amount if the coupon code is invalid or expired
  def apply_coupon(total, code)
    # TODO
  end

  # @param total [Float] must be >= 0
  # @return [Boolean] true if the purchase was successfully finalized and completed
  # @return [Boolean] false if the finalization failed due to payment error or insufficient inventory
  # @raise [ArgumentError] the param total is negative
  def finalize(total)
    # TODO
  end

end