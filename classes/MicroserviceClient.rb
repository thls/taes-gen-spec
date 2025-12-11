class MicroserviceClient
  # @param service_name [String] must be a registered microservice name
  # @param endpoint [String] must be a valid API endpoint path starting with /
  # @param method [String] must be one of: GET, POST, PUT, DELETE
  # @param params [Hash] must be a hash with request parameters
  # @param headers [Hash] must be a hash with HTTP headers
  # @param timeout [Integer] must be a positive integer between 1 and 300 seconds
  # @return [Hash] a hash containing the service response if the call was successful
  # @return [Hash] a hash with error information if the service call failed
  # @raise [ArgumentError] the param service_name is empty or not registered
  # @raise [ArgumentError] the param endpoint is not a valid path
  # @raise [ArgumentError] the param method is not a supported HTTP method
  # @raise [ArgumentError] the param timeout is not within the allowed range
  # @raise [TimeoutError] the service call exceeded the specified timeout
  def call_service(service_name, endpoint, method, params, headers, timeout)
    # TODO
  end

end