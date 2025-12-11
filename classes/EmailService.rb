class EmailService
  # @param to [String] must include @
  # @param subject [String]
  # @param body [String]
  # @return [Boolean] true if the email was successfully sent
  # @return [Boolean] false if sending failed
  def send_email(to, subject, body)
    # TODO
  end

  # @param to [String]
  # @param body [String]
  # @return [NilClass] nil after the operation completes
  def queue_email(to, body)
    # TODO
  end

end