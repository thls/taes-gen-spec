class EventBus
  # @param event [String]
  # @param payload [Hash]
  # @return [Boolean] true if the event was successfully published
  # @return [Boolean] false if publishing failed
  def publish(event, payload)
    # TODO
  end

  # @param event [String]
  # @param handler [Object]
  # @return [NilClass] nil after the operation completes
  def subscribe(event, handler)
    # TODO
  end

  # @param event [Object]
  # @return [Boolean] true if the operation succeeded
  # @return [Boolean] false if the operation failed
  def publish(event)
    # TODO
  end

  # @param name [String]
  # @param callback [Object]
  # @return [Integer] the subscribe result as an integer
  def subscribe(name, callback)
    # TODO
  end

end