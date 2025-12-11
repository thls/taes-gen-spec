class AccountManager
  # @param username [String] must not be empty
  # @param email [String] must contain @
  # @return [Hash] a hash containing the created account information
  # @raise [ArgumentError] the param email does not have the '@' character in itself
  def create_account(username, email)
    # TODO
  end

  # @param user_id [Integer] must be positive
  # @return [Boolean] true if the account was successfully suspended
  # @return [Boolean] false if the user_id does not exist or the suspension failed
  def suspend_account(user_id)
    # TODO
  end

end