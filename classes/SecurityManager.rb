class SecurityManager
  # @param user [Object] must not be nil and must have valid user attributes
  # @param resource [String] must not be empty and must be a valid resource path
  # @param action [String] must be one of: read, write, delete, execute
  # @param context [Hash] must be a hash containing authorization context information
  # @return [Boolean] true if the user is authorized to perform the action on the resource
  # @return [Boolean] false if the user is not authorized or validation failed
  # @raise [ArgumentError] the param user is nil or does not have required attributes
  # @raise [ArgumentError] the param resource is empty or invalid
  # @raise [ArgumentError] the param action is not one of the supported actions
  # @raise [SecurityError] a security violation was detected during authorization
  def validate_and_authorize(user, resource, action, context)
    # TODO
  end

end